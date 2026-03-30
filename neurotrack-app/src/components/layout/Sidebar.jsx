import { motion } from 'framer-motion';
import { LayoutDashboard, CheckSquare, BarChart2, Settings, Orbit } from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'tracker', label: 'Daily Tracker', icon: CheckSquare },
  { id: 'analytics', label: 'Analytics', icon: BarChart2 },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-black/40 backdrop-blur-2xl border-r border-white/5 flex flex-col p-6 z-50">
      <div className="flex items-center gap-3 mb-10 text-xl font-bold tracking-tight text-white">
        <Orbit className="text-primary animate-[spin_4s_linear_infinite]" size={28} />
        <span className="bg-gradient-to-r from-primary via-white to-secondary bg-clip-text text-transparent">
          NeuroTrack AI
        </span>
      </div>

      <nav className="flex-1 flex flex-col gap-2 relative">
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={clsx(
                'relative flex items-center gap-3 px-4 py-3 rounded-xl transition-colors duration-300 text-sm font-medium outline-none',
                isActive ? 'text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'
              )}
            >
              <Icon size={18} className={isActive ? 'text-accent relative z-10' : 'relative z-10'} />
              <span className="relative z-10">{item.label}</span>
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 bg-white/10 border border-white/10 rounded-xl"
                  initial={false}
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
            </button>
          );
        })}
      </nav>

      <div className="mt-auto">
        <div className="p-4 rounded-xl bg-gradient-to-br from-accent/20 to-primary/10 border border-accent/20 shadow-[0_0_20px_rgba(16,185,129,0.1)]">
          <p className="text-xs text-accent font-semibold uppercase tracking-wider mb-1">PRO PLAN</p>
          <p className="text-sm text-gray-300">All features unlocked.</p>
        </div>
      </div>
    </aside>
  );
}
