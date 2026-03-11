import React, { useState } from 'react';
import { User, Mail, Calendar, MapPin, Briefcase, Award, Code, GitBranch, Camera, Edit2, Save } from 'lucide-react';

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    name: 'John Doe',
    email: 'john.doe@aidevagent.com',
    bio: 'Full-stack developer passionate about AI and automation',
    location: 'San Francisco, CA',
    company: 'Tech Corp',
    role: 'Senior Developer',
    joinDate: 'January 2024',
    avatar: null
  });

  const handleSave = () => {
    setIsEditing(false);
    // Save profile logic here
    alert('Profile updated successfully!');
  };

  const handleChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const stats = [
    { label: 'Tasks Completed', value: '127', icon: Code, color: 'text-accent-blue' },
    { label: 'Lines of Code', value: '45.2K', icon: GitBranch, color: 'text-accent-purple' },
    { label: 'Projects', value: '23', icon: Briefcase, color: 'text-accent-green' },
    { label: 'Achievements', value: '15', icon: Award, color: 'text-yellow-500' }
  ];

  const recentActivity = [
    { task: 'Built REST API for E-commerce', date: '2 hours ago', status: 'completed' },
    { task: 'Created Authentication System', date: '1 day ago', status: 'completed' },
    { task: 'Implemented Chat Feature', date: '3 days ago', status: 'completed' },
    { task: 'Database Schema Design', date: '5 days ago', status: 'completed' }
  ];

  const badges = [
    { name: 'Early Adopter', icon: '🚀', description: 'Joined in the first 1000 users' },
    { name: 'Code Master', icon: '💻', description: 'Generated 10K+ lines of code' },
    { name: 'Quick Learner', icon: '⚡', description: 'Completed 100+ tasks' },
    { name: 'Bug Hunter', icon: '🐛', description: 'Fixed 50+ bugs' },
    { name: 'AI Pioneer', icon: '🤖', description: 'Used all AI features' },
    { name: 'Team Player', icon: '🤝', description: 'Collaborated on 10+ projects' }
  ];

  return (
    <div className="min-h-screen bg-dark-primary pt-16">
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Profile Header */}
        <div className="bg-dark-secondary border border-dark-border rounded-xl overflow-hidden mb-8">
          {/* Cover Image */}
          <div className="h-32 bg-gradient-to-r from-accent-blue to-accent-purple relative">
            <button className="absolute top-4 right-4 p-2 bg-black/30 hover:bg-black/50 rounded-lg transition-colors backdrop-blur-sm">
              <Camera size={18} />
            </button>
          </div>

          {/* Profile Info */}
          <div className="px-8 pb-8">
            <div className="flex flex-col md:flex-row md:items-end md:justify-between -mt-16 mb-6">
              <div className="flex flex-col md:flex-row md:items-end gap-6">
                {/* Avatar */}
                <div className="relative">
                  <div className="w-32 h-32 rounded-xl border-4 border-dark-secondary bg-gradient-to-br from-accent-blue to-accent-purple flex items-center justify-center text-4xl font-bold">
                    {profileData.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <button className="absolute bottom-2 right-2 p-2 bg-accent-blue hover:bg-accent-blue/80 rounded-lg transition-colors">
                    <Camera size={16} />
                  </button>
                </div>

                {/* Name & Bio */}
                <div className="flex-1 space-y-2 mt-4 md:mt-0">
                  {isEditing ? (
                    <>
                      <input
                        type="text"
                        value={profileData.name}
                        onChange={(e) => handleChange('name', e.target.value)}
                        className="text-3xl font-bold bg-dark-tertiary border border-dark-border rounded-lg px-3 py-2 w-full focus:outline-none focus:border-accent-blue"
                      />
                      <textarea
                        value={profileData.bio}
                        onChange={(e) => handleChange('bio', e.target.value)}
                        className="text-gray-400 bg-dark-tertiary border border-dark-border rounded-lg px-3 py-2 w-full focus:outline-none focus:border-accent-blue resize-none"
                        rows="2"
                      />
                    </>
                  ) : (
                    <>
                      <h1 className="text-3xl font-bold">{profileData.name}</h1>
                      <p className="text-gray-400">{profileData.bio}</p>
                    </>
                  )}
                </div>
              </div>

              {/* Edit Button */}
              <div className="mt-4 md:mt-0">
                {isEditing ? (
                  <button
                    onClick={handleSave}
                    className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-accent-blue to-accent-purple rounded-xl font-semibold hover:opacity-90 transition-all"
                  >
                    <Save size={18} />
                    Save Changes
                  </button>
                ) : (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="flex items-center gap-2 px-6 py-3 bg-dark-tertiary border border-dark-border rounded-xl font-semibold hover:bg-dark-border transition-colors"
                  >
                    <Edit2 size={18} />
                    Edit Profile
                  </button>
                )}
              </div>
            </div>

            {/* Profile Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {isEditing ? (
                <>
                  <div className="flex items-center gap-3 p-3 bg-dark-tertiary rounded-lg">
                    <Mail size={20} className="text-accent-blue" />
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => handleChange('email', e.target.value)}
                      className="flex-1 bg-transparent border-none focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-dark-tertiary rounded-lg">
                    <MapPin size={20} className="text-accent-green" />
                    <input
                      type="text"
                      value={profileData.location}
                      onChange={(e) => handleChange('location', e.target.value)}
                      className="flex-1 bg-transparent border-none focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-dark-tertiary rounded-lg">
                    <Briefcase size={20} className="text-accent-purple" />
                    <input
                      type="text"
                      value={profileData.company}
                      onChange={(e) => handleChange('company', e.target.value)}
                      className="flex-1 bg-transparent border-none focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-dark-tertiary rounded-lg">
                    <User size={20} className="text-yellow-500" />
                    <input
                      type="text"
                      value={profileData.role}
                      onChange={(e) => handleChange('role', e.target.value)}
                      className="flex-1 bg-transparent border-none focus:outline-none"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-3">
                    <Mail size={20} className="text-accent-blue flex-shrink-0" />
                    <span className="text-gray-400 truncate">{profileData.email}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <MapPin size={20} className="text-accent-green flex-shrink-0" />
                    <span className="text-gray-400">{profileData.location}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Briefcase size={20} className="text-accent-purple flex-shrink-0" />
                    <span className="text-gray-400">{profileData.company}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Calendar size={20} className="text-yellow-500 flex-shrink-0" />
                    <span className="text-gray-400">Joined {profileData.joinDate}</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {stats.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div key={index} className="bg-dark-secondary border border-dark-border rounded-xl p-6 text-center">
                    <Icon size={24} className={`${stat.color} mx-auto mb-3`} />
                    <div className="text-2xl font-bold mb-1">{stat.value}</div>
                    <div className="text-sm text-gray-400">{stat.label}</div>
                  </div>
                );
              })}
            </div>

            {/* Recent Activity */}
            <div className="bg-dark-secondary border border-dark-border rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-6">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start gap-4 pb-4 border-b border-dark-border last:border-0 last:pb-0">
                    <div className="w-2 h-2 rounded-full bg-accent-green mt-2 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="font-medium mb-1">{activity.task}</p>
                      <p className="text-sm text-gray-400">{activity.date}</p>
                    </div>
                    <span className="px-3 py-1 bg-accent-green/20 text-accent-green rounded-full text-xs">
                      {activity.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Badges */}
          <div className="space-y-8">
            <div className="bg-dark-secondary border border-dark-border rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-6">Achievements</h2>
              <div className="grid grid-cols-2 gap-4">
                {badges.map((badge, index) => (
                  <div
                    key={index}
                    className="bg-dark-tertiary border border-dark-border rounded-xl p-4 text-center hover:border-accent-blue transition-colors cursor-pointer group"
                    title={badge.description}
                  >
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">{badge.icon}</div>
                    <div className="text-xs font-medium">{badge.name}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Skills */}
            <div className="bg-dark-secondary border border-dark-border rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-6">Top Skills</h2>
              <div className="space-y-4">
                {['JavaScript', 'Python', 'React', 'Node.js', 'AI/ML'].map((skill, index) => (
                  <div key={index}>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium">{skill}</span>
                      <span className="text-sm text-gray-400">{90 - index * 10}%</span>
                    </div>
                    <div className="w-full bg-dark-tertiary rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-accent-blue to-accent-purple h-2 rounded-full transition-all"
                        style={{ width: `${90 - index * 10}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
