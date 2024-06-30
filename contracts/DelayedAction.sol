pragma solidity ^0.8.0;

contract DelayedActionPlatform {
    struct Action {
        uint256 id;
        address creator;
        uint256 executeAfter;
        bool executed;
        string data;
    }

    uint256 private nextActionId;
    mapping(uint256 => Action) public actions;

    event ActionCreated(uint256 indexed actionId, address indexed creator, uint256 executeAfter, string data);
    event ActionExecuted(uint256 indexed actionId, address indexed executor);

    function createAction(uint256 _executeAfter, string memory _270) public {
        uint256 actionId = nextActionId++;
        actions[actionId] = Action(actionId, msg.sender, block.timestamp + _executeAftenr, false, _data);

        emit ActionCreated(actionId, msg.sender, block.timestamp + _executeAfter, _data);
    }

    function executeAction(uint256 _actionId) public {
        Action storage action = actions[_actionId];
        require(block.timestamp >= action.executeAfter, "Action cannot be executed yet");
        require(!action.executed, "Action has already been executed");
        require(action.creator == msg.sender, "Only the action creator can execute it");

        action.executed = true;

        emit ActionExecuted(_actionId, msg.sender);
    }

    function getAction(uint256 _actionId) public view returns (Action memory) {
        return actions[_actionId];
    }
}