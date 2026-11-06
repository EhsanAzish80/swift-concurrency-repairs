import Testing
@testable import Kingfisher

@Suite(.serialized)
struct ResearchRepro {
    private func cancel(_ bridge: CancellationDownloadTask) async {
        #if REPRO_FAULTY
        // Exact old onCancel action, awaited so cancellation runs before attachment.
        await bridge.task?.cancel()
        #else
        bridge.cancel()
        #endif
    }
    private func attach(_ bridge: CancellationDownloadTask, _ task: DownloadTask) async {
        #if REPRO_FAULTY
        await bridge.setTask(task)
        #else
        bridge.setTask(task)
        #endif
    }
    @Test func cancellationBeforeAttachmentIsRemembered() async {
        for iteration in 0..<100 {
            let underlying = Task<Void, Never> { }
            let task = DownloadTask(providerTask: underlying)
            let bridge = CancellationDownloadTask()
            await cancel(bridge)
            await attach(bridge, task)
            #expect(underlying.isCancelled, "cancel-before-attach iteration \(iteration)")
            underlying.cancel()
            await underlying.value
        }
    }
    @Test func cancellationAfterAttachmentControl() async {
        for _ in 0..<100 {
            let underlying = Task<Void, Never> { }
            let task = DownloadTask(providerTask: underlying)
            let bridge = CancellationDownloadTask()
            await attach(bridge, task)
            await cancel(bridge)
            #expect(underlying.isCancelled)
            await underlying.value
        }
    }
    @Test func noCancellationControl() async {
        for _ in 0..<100 {
            let underlying = Task<Void, Never> { }
            let task = DownloadTask(providerTask: underlying)
            let bridge = CancellationDownloadTask()
            await attach(bridge, task)
            #expect(!underlying.isCancelled)
            underlying.cancel()
            await underlying.value
        }
    }
}
