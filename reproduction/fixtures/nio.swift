import XCTest
import DequeModule
@testable import NIOCore

private struct ResearchDelegate: NIOAsyncWriterSinkDelegate {
    typealias Element = String
    func didYield(contentsOf sequence: Deque<String>) { }
    func didTerminate(error: Error?) { }
}
final class ResearchRepro: XCTestCase {
    func testCancelledBeforeRegistrationIsCaughtBySecondCheck() {
        typealias SM = NIOAsyncWriter<String, ResearchDelegate>.StateMachine
        for idValue in 0..<100 {
            var machine = SM(isWritable: false, delegate: ResearchDelegate())
            let id = SM.YieldID(value: UInt64(idValue))
            guard case .suspendTask = machine.yield(yieldID: id) else {
                return XCTFail("Initial check did not suspend")
            }
            // Cancellation in the unlocked interval before continuation registration.
            _ = machine.cancel(yieldID: id)
            // Production performs this check while holding the same lock as registration.
            guard case .throwError(let error) = machine.yield(yieldID: id) else {
                return XCTFail("Cancellation lost by production second check")
            }
            XCTAssertTrue(error is CancellationError)
        }
    }
    func testPublicWriterCancellationCompletes() async {
        for _ in 0..<100 {
            let pair = NIOAsyncWriter.makeWriter(elementType: String.self,
                isWritable: false, finishOnDeinit: false, delegate: ResearchDelegate())
            let task = Task { try await pair.writer.yield("value") }
            task.cancel()
            do { try await task.value; XCTFail("Expected cancellation") }
            catch { XCTAssertTrue(error is CancellationError) }
            pair.sink.finish()
            pair.writer.finish()
        }
    }
}
