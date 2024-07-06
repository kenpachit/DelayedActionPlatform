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
    event ActionExecuted(uint256 indexed actionId, address executor);

    error ExecuteAfterMustBePositive();
    error ActionDoesNotExist(uint256 actionId);
    error ActionCannotBeExecutedYet(uint256 actionId);
    error ActionAlreadyExecuted(uint256 actionId);
    error OnlyCreatorCanExecute(uint256 actionId);

    function createAction(uint256 _executeAfter, string memory _data) public {
        if (_executeAfter == 0) revert ExecuteAfterMustBePositive();

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

    function executeAction(uint256 _actionId) public {
        if (_actionId >= nextActionId) revert ActionDoesNotExist(_actionId);
        Action storage action = actions[_actionId];

        if (block.timestamp < action.executeAfter) revert ActionCannotBeExecutedYet(_actionId);
        if (action.executed) revert ActionAlreadyExecuted(_actionId);
        if (action.creator != msg.sender) revert OnlyCreatorCanExecute(_actionId);

        action.executed = true;

        emit ActionExecuted(_actionId, msg.sender);
    }

    function getAction(uint256 _actionId) public view returns (Action memory) {
        if (_actionId >= nextActionId) revert ActionDoesNotExist(_actionId);
        return actions[_actionId];
    }
}