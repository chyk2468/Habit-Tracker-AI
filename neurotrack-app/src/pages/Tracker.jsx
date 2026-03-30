import { motion, AnimatePresence } from 'framer-motion';
import { getTodayStr } from '../hooks/useNeuroData';
import { Check, Circle } from 'lucide-react';
import clsx from 'clsx';
import confetti from 'canvas-confetti';

export function Tracker({ neuro }) {
  const todayStr = getTodayStr();
  const dayData = neuro.data.history[todayStr] || { habits: {}, score: 0 };
  const tasks = Object.keys(dayData.habits);

  const handleToggle = (task) => {
    neuro.toggleHabit(todayStr, task);
    
    // Confetti logic
    const currentHabits = { ...dayData.habits, [task]: !dayData.habits[task] };
    const completed = Object.values(currentHabits).filter(Boolean).length;
    if (completed === tasks.length && completed > 0) {
      confetti({
        particleCount: 150,
        spread: 90,
        origin: { y: 0.6 },
        colors: ['#00f2fe', '#4facfe', '#10b981', '#8b5cf6']
      });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3 }}
      className="max-w-4xl mx-auto pb-20"
    >
      <header className="mb-10">
        <h2 className="text-4xl font-extrabold tracking-tight mb-2 text-white">Daily <span className="text-accent">Protocol</span></h2>
        <p className="text-lg text-gray-400 font-medium">Execute your optimal schedule.</p>
      </header>

      <div className="glass-card mb-12 overflow-hidden relative">
        <div className="flex justify-between items-end mb-4 relative z-10">
          <h3 className="text-xl font-bold text-white tracking-wide uppercase text-gray-400 text-sm">Completion Rate</h3>
          <span className="text-5xl font-extrabold text-accent">{dayData.score}%</span>
        </div>
        
        <div className="h-4 bg-white/5 rounded-full overflow-hidden relative z-10">
          <motion.div 
            className="h-full bg-gradient-to-r from-accent to-primary"
            initial={{ width: 0 }}
            animate={{ width: `${dayData.score}%` }}
            transition={{ type: "spring", stiffness: 50, damping: 15 }}
          />
        </div>
        <div className="absolute -bottom-10 -right-10 w-48 h-48 bg-accent/20 blur-3xl rounded-full pointer-events-none" />
      </div>

      <div className="relative pl-2">
        {/* Timeline Line */}
        <div className="absolute left-[34px] top-8 bottom-8 w-[2px] bg-white/10 z-0" />
        
        <div className="flex flex-col gap-6 relative z-10">
          <AnimatePresence>
            {tasks.map((task, idx) => {
              const isDone = dayData.habits[task];
              
              return (
                <motion.div
                  key={task}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="flex items-center gap-8 group"
                >
                  <button
                    onClick={() => handleToggle(task)}
                    className={clsx(
                      "w-12 h-12 rounded-full flex flex-shrink-0 items-center justify-center border-2 transition-all duration-300 z-10",
                      isDone 
                        ? "bg-accent border-accent text-[#0B0F1A] shadow-[0_0_20px_rgba(16,185,129,0.5)] scale-110" 
                        : "bg-[#0B0F1A] border-white/20 text-gray-500 hover:border-accent/80 hover:text-accent"
                    )}
                  >
                    <motion.div
                      initial={false}
                      animate={{ scale: isDone ? [0, 1.4, 1] : 1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Check size={24} strokeWidth={isDone ? 4 : 2} className={!isDone ? "opacity-0 group-hover:opacity-100 transition-opacity" : ""} />
                    </motion.div>
                  </button>
                  
                  <div className={clsx(
                    "flex-1 glass-card p-5 !mb-0 transition-opacity duration-300 cursor-pointer flex items-center min-h-[5rem]",
                    isDone ? "opacity-50" : "hover:border-white/20"
                  )}
                  onClick={() => handleToggle(task)}
                  >
                    <span className={clsx("text-lg font-medium tracking-wide transition-all duration-300", isDone ? "line-through text-gray-500" : "text-gray-100")}>
                      {task}
                    </span>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
}
