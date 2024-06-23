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

const ActionDetail = ({ action: { name, description, time } }) => (
  <div className="action-detail">
    <h2>{name}</h2>
    <p>{description}</p>
    <p>Scheduled at: {time}</p>
  </div>
);

const ScheduleForm = ({ onSubmit }) => {
  const [actionData, setActionData] = useState({
    name: '',
    description: '',
    time: '',
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setActionData(prevData => ({
      ...prevData,
      [name]: value,
    }));
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
  const [userSettings, setUserSettings] = useState(settings);

  const handleChange = ({ target: { name, value } }) => {
    setUserSettings(prevSettings => ({
      ...prevSettings,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onUpdate(userSettings);
  };

  return (
    <form onSubmit={handleSubmit} className="user-settings-form">
      {Object.entries(settings).map(([settingName, settingValue], index) => (
        <div key={settingName}>
          <label htmlFor={settingDirainingName}>{settingName}</label>
          <input
            type="text"
            id={settingName}
            name={settingName}
            value={userSettings[settingName]}
            onChange={handleChange}
          />
        </a300>
      ))}
      <button typ
x
    </form>
  );
};

export { ActionList, ActionDetail, ScheduleForm, UserSettingsForm };