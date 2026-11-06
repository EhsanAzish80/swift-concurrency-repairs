import Testing
import AppKit
@testable import Nuke

@Suite(.serialized)
struct ResearchRepro {
    @Test @ImagePipelineActor func immediateMemoryHitKeepsTerminalEvent() async throws {
        for iteration in 0..<20 {
            let pipeline = ImagePipeline { $0.imageCache = ImageCache() }
            let request = ImageRequest(url: URL(string: "https://repro.invalid/image")!)
            pipeline.cache[request] = ImageContainer(image: NSImage(size: NSSize(width: 2, height: 2)))
            let task = pipeline.imageTask(with: request)
            var terminal = 0
            for await event in task.events {
                if case .finished = event { terminal += 1 }
            }
            #expect(terminal == 1, "immediate memory hit iteration \(iteration)")
            #expect(task.status.result != nil)
        }
    }
    @Test @ImagePipelineActor func completedTaskReplaysTerminalEvent() async throws {
        for iteration in 0..<20 {
            let pipeline = ImagePipeline { $0.imageCache = ImageCache() }
            let request = ImageRequest(url: URL(string: "https://repro.invalid/image")!)
            pipeline.cache[request] = ImageContainer(image: NSImage(size: NSSize(width: 2, height: 2)))
            let task = pipeline.imageTask(with: request)
            _ = try await task.response
            var terminal = 0
            for await event in task.events {
                if case .finished = event { terminal += 1 }
            }
            #expect(terminal == 1, "late subscriber iteration \(iteration)")
        }
    }
}
