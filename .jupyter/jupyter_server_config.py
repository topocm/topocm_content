import asyncio
import os

from jupyter_server.services.kernels.kernelmanager import AsyncMappingKernelManager
from traitlets import Integer, observe


class LimitingKernelManager(AsyncMappingKernelManager):
    """
    Kernel manager that caps how many kernels exist at once.

    - max_kernels: maximum number of live kernels.
    - Each started kernel acquires a slot.
    - Each shutdown (or shutdown_all) releases slots.
    """

    max_kernels = Integer(
        4,  # set your default here
        config=True,
        help="Maximum number of kernels that may run concurrently.",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # semaphore with 'max_kernels' slots, each slot == one live kernel
        self._kernel_slots = asyncio.Semaphore(self.max_kernels)

    @observe("max_kernels")
    def _on_max_kernels_changed(self, change):
        # if config changes, reset semaphore; simplest is to recreate it
        self._kernel_slots = asyncio.Semaphore(change["new"])

    async def start_kernel(self, *args, **kwargs):
        # Wait for a free slot; this is atomic across concurrent requests.
        await self._kernel_slots.acquire()
        try:
            kernel_id = await super().start_kernel(*args, **kwargs)
        except Exception:
            # If startup failed, free the slot again.
            self._kernel_slots.release()
            raise
        return kernel_id

    async def shutdown_kernel(self, kernel_id, *args, **kwargs):
        try:
            return await super().shutdown_kernel(kernel_id, *args, **kwargs)
        finally:
            # Kernel is gone -> free a slot.
            self._kernel_slots.release()

    async def shutdown_all(self, *args, **kwargs):
        try:
            return await super().shutdown_all(*args, **kwargs)
        finally:
            # All kernels gone -> reset semaphore to full capacity.
            self._kernel_slots = asyncio.Semaphore(self.max_kernels)


c = get_config()  # noqa: F821
c.ServerApp.ip = "127.0.0.1"  # Needed to specify explicitly to avoid binding to ::1.
c.ServerApp.allow_root = True  # CI often runs as root inside containers.
c.ServerApp.kernel_manager_class = LimitingKernelManager

# Respect JUPYTER_NUM_PROCS environment variable if set. This allows CI (e.g.
# .gitlab-ci.yml) to cap the number of concurrent kernels during execution.
env_val = os.getenv("JUPYTER_NUM_PROCS")
if env_val:
    try:
        parsed = int(env_val)
        # Enforce a sensible minimum of 1.
        c.LimitingKernelManager.max_kernels = max(1, parsed)
    except Exception:
        # If parsing fails, fall back to the default of 4.
        c.LimitingKernelManager.max_kernels = 4
else:
    c.LimitingKernelManager.max_kernels = 4
