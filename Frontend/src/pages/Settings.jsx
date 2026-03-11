import React, { useState } from 'react';
import { Settings as SettingsIcon, User, Bell, Palette, Code, Save } from 'lucide-react';

const Settings = () => {
  const [settings, setSettings] = useState({
    name: 'Developer',
    email: 'developer@aidevagent.com',
    notifications: true,
    autoSave: true,
    theme: 'dark',
    language: 'javascript',
    aiModel: 'gpt-4'
  });
  
  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };
  
  const handleSave = () => {
    // Save settings logic
    alert('Settings saved successfully!');
  };
  
  return (
    <div className="min-h-screen bg-dark-primary pt-16">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <SettingsIcon size={32} className="text-accent-purple" />
            <h1 className="text-3xl font-bold">Settings</h1>
          </div>
          <p className="text-gray-400">Customize your AI Dev Agent experience</p>
        </div>
        
        <div className="space-y-6">
          {/* Profile Settings */}
          <section className="bg-dark-secondary border border-dark-border rounded-xl p-6">
            <div className="flex items-center gap-2 mb-6">
              <User size={20} className="text-accent-blue" />
              <h2 className="text-xl font-semibold">Profile</h2>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Name</label>
                <input
                  type="text"
                  value={settings.name}
                  onChange={(e) => handleChange('name', e.target.value)}
                  className="w-full px-4 py-3 bg-dark-tertiary border border-dark-border rounded-lg text-white focus:outline-none focus:border-accent-blue"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={settings.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  className="w-full px-4 py-3 bg-dark-tertiary border border-dark-border rounded-lg text-white focus:outline-none focus:border-accent-blue"
                />
              </div>
            </div>
          </section>
          
          {/* Preferences */}
          <section className="bg-dark-secondary border border-dark-border rounded-xl p-6">
            <div className="flex items-center gap-2 mb-6">
              <Palette size={20} className="text-accent-purple" />
              <h2 className="text-xl font-semibold">Preferences</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Notifications</p>
                  <p className="text-sm text-gray-400">Receive updates about your tasks</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.notifications}
                    onChange={(e) => handleChange('notifications', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-dark-tertiary peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-blue"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Auto Save</p>
                  <p className="text-sm text-gray-400">Automatically save your progress</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.autoSave}
                    onChange={(e) => handleChange('autoSave', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-dark-tertiary peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-blue"></div>
                </label>
              </div>
            </div>
          </section>
          
          {/* AI Configuration */}
          <section className="bg-dark-secondary border border-dark-border rounded-xl p-6">
            <div className="flex items-center gap-2 mb-6">
              <Code size={20} className="text-accent-green" />
              <h2 className="text-xl font-semibold">AI Configuration</h2>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Default Language</label>
                <select
                  value={settings.language}
                  onChange={(e) => handleChange('language', e.target.value)}
                  className="w-full px-4 py-3 bg-dark-tertiary border border-dark-border rounded-lg text-white focus:outline-none focus:border-accent-blue"
                >
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="python">Python</option>
                  <option value="java">Java</option>
                  <option value="go">Go</option>
                  <option value="rust">Rust</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">AI Model</label>
                <select
                  value={settings.aiModel}
                  onChange={(e) => handleChange('aiModel', e.target.value)}
                  className="w-full px-4 py-3 bg-dark-tertiary border border-dark-border rounded-lg text-white focus:outline-none focus:border-accent-blue"
                >
                  <option value="gpt-4">GPT-4 (Most Capable)</option>
                  <option value="gpt-3.5">GPT-3.5 (Faster)</option>
                  <option value="claude">Claude (Alternative)</option>
                </select>
              </div>
            </div>
          </section>
          
          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-accent-blue to-accent-purple rounded-xl font-semibold hover:opacity-90 transition-opacity"
            >
              <Save size={20} />
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
