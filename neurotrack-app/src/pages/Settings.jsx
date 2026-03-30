import { motion } from 'framer-motion';
import { User, Bell, Shield, Palette } from 'lucide-react';
import clsx from 'clsx';
import { useState } from 'react';

export function Settings() {
  const [theme, setTheme] = useState('dark');
  const [notifications, setNotifications] = useState(true);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4 }}
      className="max-w-4xl mx-auto"
    >
      <header className="mb-10">
        <h2 className="text-4xl font-extrabold tracking-tight mb-2 text-white">System <span className="text-gray-500">Settings</span></h2>
        <p className="text-lg text-gray-400 font-medium">Configure your NeuroTrack environment.</p>
      </header>

      <div className="grid gap-6">
        {/* Profile */}
        <div className="glass-card flex items-center justify-between p-6 hover:border-white/20">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center p-0.5">
              <div className="w-full h-full bg-[#0B0F1A] rounded-2xl flex items-center justify-center relative overflow-hidden group hover:bg-transparent transition-colors duration-300">
                 <User className="text-primary group-hover:text-white transition-colors" size={24} />
              </div>
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Guest User</h3>
              <p className="text-sm text-gray-400">Local Storage Mode</p>
            </div>
          </div>
          <button className="px-5 py-2.5 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 text-white font-medium transition-all duration-300 active:scale-95">
            Edit Profile
          </button>
        </div>

        {/* Preferences */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Palette size={18} className="text-gray-400" /> Preferences
          </h3>
          
          <div className="flex items-center justify-between py-4 border-b border-white/5">
            <div>
              <h4 className="font-semibold text-gray-200">Theme Preference</h4>
              <p className="text-sm text-gray-500">Choose your interface style.</p>
            </div>
            <div className="flex bg-black/40 p-1 rounded-xl border border-white/5">
               <button 
                  onClick={() => setTheme('dark')}
                  className={clsx("px-4 py-2 rounded-lg text-sm font-medium transition-all", theme === 'dark' ? "bg-white/10 text-white shadow-md shadow-black" : "text-gray-500 hover:text-gray-300")}
               >
                 Dark
               </button>
               <button 
                  onClick={() => setTheme('light')}
                  className={clsx("px-4 py-2 rounded-lg text-sm font-medium transition-all opacity-50 cursor-not-allowed")}
               >
                 Light
               </button>
            </div>
          </div>

          <div className="flex items-center justify-between py-4">
            <div>
              <h4 className="font-semibold text-gray-200">System Notifications</h4>
              <p className="text-sm text-gray-500">Get alerts for schedule changes.</p>
            </div>
            <button 
              onClick={() => setNotifications(!notifications)}
              className={clsx(
                "w-12 h-6 rounded-full relative transition-colors duration-300",
                notifications ? "bg-accent" : "bg-white/10"
              )}
            >
               <div className={clsx(
                 "absolute top-1 w-4 h-4 bg-white rounded-full transition-transform duration-300 shadow-sm",
                 notifications ? "left-7" : "left-1"
               )} />
            </button>
          </div>
        </div>

        {/* Security */}
        <div className="glass-card p-6 opacity-60">
           <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Shield size={18} className="text-gray-400" /> Data & Privacy
          </h3>
          <p className="text-sm text-gray-400 mb-4">Your productivity data is stored securely in your browser's local storage. Clearing site data will reset your history.</p>
          <button className="px-5 py-2.5 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20 font-medium transition-colors">
            Clear Local Data
          </button>
        </div>
      </div>
    </motion.div>
  );
}
