import React from 'react';

const ActionList = ({ actions }) => {
  return (
    <div className="action-list">
      {actions.map((action, index) => (
        <div key={index} className="action-item">
          {action.name}
        </div>
      ))}
    </div>
  );
};

const ActionDetail = ({ action }) => {
  return (
    <div className="action-detail">
      <h2>{action.name}</h2>
      <p>{action.description}</p>
      <p>Scheduled at: {action.time}</p>
    </div>
  );
};

const ScheduleForm = ({ onSubmit }) => {
  const [actionData, setActionData] = React.useState({
    name: '',
    description: '',
    time: '',
  });

  const handleChange = (event) => {
    setActionData({
      ...actionData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(actionData);
  };

  return (
    <form onSubmit={handleSubmit} className="schedule-form">
      <input
        type="text"
        name="name"
        placeholder="Action Name"
        value={actionData.name}
        onChange={handleChange}
      />
      <textarea
        name="description"
        placeholder="Action Description"
        value={actionData.description}
        onChange={handleChange}
      />
      <input
        type="datetime-local"
        name="time"
        value={actionData.time}
        onChange={handleChange}
      />
      <button type="submit">Schedule Action</button>
    </form>
  );
};

const UserSettingsForm = ({ settings, onUpdate }) => {
  const [userSettings, setUserSettings] = React.useState(settings);

  const handleChange = (event) => {
    setUserSettings({
      ...userSettings,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onUpdate(userSettings);
  };

  return (
    <form onSubmit={handleSubmit} className="user-settings-form">
      {Object.keys(settings).map((settingName, index) => (
        <div key={index}>
          <label htmlFor={settingName}>{settingName}</label>
          <input
            type="text"
            id={settingName}
            name={settingName}
            value={userSettings[settingName]}
            onChange={handleChange}
          />
        </div>
      ))}
      <button type="submit">Update Settings</button>
    </form>
  );
};

export { ActionList, ActionDetail, ScheduleForm, UserSettingsForm };