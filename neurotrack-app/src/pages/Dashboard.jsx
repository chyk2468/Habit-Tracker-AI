import { motion } from 'framer-motion';
import { StatCard } from '../components/ui/StatCard';
import { Heatmap } from '../components/ui/Heatmap';
import { Zap, Flame, Diamond, Activity, BrainCircuit } from 'lucide-react';
import { getTodayStr } from '../hooks/useNeuroData';
import clsx from 'clsx';

export function Dashboard({ neuro }) {
  const todayStr = getTodayStr();
  const dayData = neuro.data.history[todayStr];
  const todayScore = dayData ? dayData.score : 0;
  
  const status = neuro.getStatus(todayScore);
  const streak = neuro.getStreak();
  const perfectDays = neuro.getPerfectDays();
  const avgScore = neuro.getAverageScore();

  const getInsight = (score) => {
    if (score === 100) return "You're on fire! 🔥 An absolute productivity machine today. System running at optimal capacity.";
    if (score >= 60) return "Solid progress! 🚀 Push a bit more to achieve perfection today. You're outperforming your weekly average.";
    if (score > 0) return "You've started, which is the hardest part. Let's conquer those tasks. ⚡";
    return "A fresh day! Remember: small consistent steps compound into massive results. 🌌";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4 }}
      className="max-w-7xl mx-auto"
    >
      <header className="mb-12">
        <div className="flex items-center gap-4 mb-3">
          <h1 className="text-5xl font-extrabold tracking-tight">
            NeuroTrack <span className="bg-gradient-to-br from-primary via-white to-secondary bg-clip-text text-transparent">AI</span>
          </h1>
          <div className={clsx("px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border", status.color)}>
            <span className="mr-2">●</span> {status.text}
          </div>
        </div>
        <p className="text-lg text-gray-400 font-medium">Your futuristic central command for productivity.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Today's Score" value={todayScore} label="%" icon={Zap} colorClass="text-primary" glowClass="bg-primary" />
        <StatCard title="Current Streak" value={streak} label="Days" icon={Flame} colorClass="text-accent" glowClass="bg-accent" />
        <StatCard title="Perfect Days" value={perfectDays} icon={Diamond} colorClass="text-purpleGlow" glowClass="bg-purpleGlow" />
        <StatCard title="Avg Performance" value={parseFloat(avgScore)} label="%" icon={Activity} colorClass="text-amber-400" glowClass="bg-amber-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
        <div className="glass-card lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white tracking-wide">Activity <span className="text-primary">Heatmap</span></h3>
          </div>
          <Heatmap dataHistory={neuro.data.history} />
        </div>

        <div className="glass-card flex flex-col relative overflow-hidden group">
          <div className="flex items-center gap-3 mb-6 relative z-10">
            <div className="p-2 bg-purpleGlow/20 rounded-lg">
              <BrainCircuit className="text-purpleGlow" size={24} />
            </div>
            <h3 className="text-lg font-semibold text-white tracking-wide">AI <span className="text-purpleGlow">Insight</span></h3>
          </div>
          
          <div className="flex-1 flex items-center justify-center relative z-10 h-full min-h-[160px]">
            <p className="text-[1.1rem] text-gray-300 leading-relaxed font-medium italic text-center px-4 mix-blend-screen relative z-10">
              "{getInsight(todayScore)}"
            </p>
          </div>
          
          <div className="absolute top-0 right-0 w-64 h-64 bg-purpleGlow/10 blur-[80px] rounded-full group-hover:bg-purpleGlow/20 transition-colors duration-1000 z-0" />
        </div>
      </div>
    </motion.div>
  );
}
