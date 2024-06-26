import React, { useState } from 'react';

const ActionList = ({ actions }) => (
  <div className="action-list">
    {actions.map((action, index) => (
      <div key={index} className="action-item">
        {action.name}
      </div>
    ))}
  </div>
);

const ActionDetails = ({ action: { name, description, scheduledTime } }) => (
  <div className="action-detail">
    <h2>{name}</h2>
    <p>{description}</p>
    <p>Scheduled at: {scheduledTime}</p>
  </div>
);

const ScheduleActionForm = ({ onActionSubmit }) => {
  const [scheduledAction, setScheduledAction] = useState({
    name: '',
    description: '',
    time: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setScheduledAction(prevAction => ({
      ...prevAction,
      [name]: value,
    }));
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    onActionSubmit(scheduledAction);
  };

  return (
    <form onSubmit={handleFormSubmit} className="schedule-form">
      <input
        type="text"
        name="name"
        placeholder="Action Name"
        value={scheduledAction.name}
        onChange={handleInputChange}
      />
      <textarea
        name="description"
        placeholder="Action Description"
        value={scheduledAction.description}
        onChange={handleInputChange}
      />
      <input
        type="datetime-local"
        name="time"
        value={scheduledAction.time}
        onChange={handleInputChange}
      />
      <button type="submit">Schedule Action</button>
    </form>
  );
};

const UserSettingsForm = ({ initialSettings, onUpdateSettings }) => {
  const [userSettings, setUserSettings] = useState(initialSettings);

  const handleSettingsChange = ({ target: { name, value } }) => {
    setUserSettings(prevSettings => ({
      ...prevSettings,
      [name]: value,
    }));
  };

  const handleSettingsSubmit = (event) => {
    event.preventDefault();
    onUpdateSettings(userSettings);
  };

  return (
    <form onSubmit={handleSettingsSubmit} className="user-settings-form">
      {Object.entries(initialSettings).map(([settingName, settingValue]) => (
        <div key={settingName}>
          <label htmlFor={settingName}>{settingName}</label>
          <input
            type="text"
            id={settingName}
            name={settingName}
            value={userSettings[settingName]}
            onChange={handleSettingsChange}
          />
        </div>
      ))}
      <button type="submit">Update Settings</button>
    </form>
  );
};

export { ActionList, ActionDetails, ScheduleActionForm, UserSettingsForm };