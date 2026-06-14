from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
from typing import Callable, Iterable, List, TypeVar, Optional

T = TypeVar("T")
R = TypeVar("R")

logger = logging.getLogger(__name__)


class ParallelExecutor:
    """
    Executor paralelo para processamento de tarefas em lote.

    Permite aplicar uma função a uma coleção de itens de forma concorrente,
    utilizando `ThreadPoolExecutor`. Os itens são divididos em batches para
    controle de carga e, opcionalmente, pode-se inserir um delay entre os lotes.

    Esse padrão é útil para cenários de I/O-bound (ex.: chamadas a APIs,
    operações de rede ou banco de dados), onde paralelismo melhora o throughput.

    A implementação também permite controle de falhas, podendo ignorar erros
    ou propagá-los conforme configuração.
    """

    def __init__(
        self,
        max_workers: int = 5,
        batch_size: int = 10,
        delay: float = 0.0,
        preserve_order: bool = False,
    ):
        """
        Inicializa o executor paralelo.

        Args:
            max_workers (int): Número máximo de threads concorrentes por batch.
            batch_size (int): Quantidade de itens processados por lote.
            delay (float): Tempo de espera (em segundos) entre o processamento
                de batches consecutivos.
        """
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.delay = delay
        self.preserve_order = preserve_order

    def _chunk(self, items: List[T]) -> List[List[T]]:
        """
        Divide uma lista de itens em batches menores.

        Args:
            items (List[T]): Lista de itens a ser dividida.

        Returns:
            List[List[T]]: Lista de batches contendo subconjuntos dos itens.
        """
        return [
            items[i : i + self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]

    def map(
        self,
        func: Callable[[T], R],
        items: Iterable[T],
        fail_silently: bool = True,
        timeout: Optional[float] = None,
    ) -> List[R]:
        """
        Processa um batch de itens de forma paralela.

        Submete cada item do batch para execução concorrente utilizando threads
        e coleta os resultados conforme finalização das tarefas.

        Args:
            func (Callable[[T], R]): Função a ser aplicada a cada item.
            batch (List[T]): Lista de itens a serem processados.
            fail_silently (bool): Se True, ignora exceções durante o processamento;
                caso contrário, propaga a exceção.

        Returns:
            List[R]: Lista de resultados produzidos pela função aplicada aos itens.
        """
        items = list(items)
        batches = self._chunk(items)

        results: List[Optional[R]] = [None] * len(items) if self.preserve_order else []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            base_index = 0

            for batch in batches:
                future_to_index = {}

                for i, item in enumerate(batch):
                    future = executor.submit(func, item)
                    index = base_index + i
                    future_to_index[future] = index

                for future in as_completed(future_to_index):
                    idx = future_to_index[future]

                    try:
                        result = future.result(timeout=timeout)

                        if self.preserve_order:
                            results[idx] = result
                        else:
                            if result is not None:
                                results.append(result)

                    except Exception as e:
                        logger.error(f"Error processing index {idx}: {e}")

                        if not fail_silently:
                            raise

                base_index += len(batch)

                if self.delay > 0:
                    time.sleep(self.delay)

        if self.preserve_order:
            return [r for r in results if r is not None]

        return results
