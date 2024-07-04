// SPDX-License-Identifier: MIT
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

    /// @notice Creates a new delayed action
    /// @param _executeAfter Seconds to wait until the action can be executed
    /// @param _data Arbitrary data associated with the action
    function createAction(uint256 _executeAfter, string memory _data) public {
        require(_executeAfter > 0, "Execution delay must be > 0");

        uint256 actionId = nextActionId++;
        uint256 executeAfter = block.timestamp + _executeAfter;

        actions[actionId] = Action({
            id: actionId, 
            creator: msg.sender, 
            executeAfter: executeAfter, 
            executed: false, 
            data: _data
        });

        emit ActionCreated(actionId, msg.sender, executeAfter, _data);
    }

    /// @notice Executes a specified action, if conditions are met
    /// @param _actionId ID of the action to be executed
    function executeAction(uint256 _actionId) public {
        require(_actionId < nextActionId, "Action does not exist");
        Action storage action = actions[_actionId];

        require(block.timestamp >= action.executeAfter, "Action cannot be executed yet");
        require(!action.executed, "Action already executed");
        require(action.creator == msg.sender, "Only creator can execute");

        action.executed = true;

        emit ActionExecuted(_actionId, msg.sender);
    }

    /// @notice Fetches details of an action
    /// @param _actionId ID of the action to fetch
    /// @return The action details
    function getAction(uint256 _actionId) public view returns (Action memory) {
        require(_actionId < nextActionId, "Action does not work");
        return actions[_actionId];
    }
}