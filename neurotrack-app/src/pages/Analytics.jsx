import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function Analytics({ neuro }) {
  const weeklyData = neuro.getWeeklyData().reverse();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4 }}
      className="max-w-6xl mx-auto"
    >
      <header className="mb-10">
        <h2 className="text-4xl font-extrabold tracking-tight mb-2 text-white">Performance <span className="text-secondary">Analytics</span></h2>
        <p className="text-lg text-gray-400 font-medium">Deep dive into your productivity trajectories.</p>
      </header>

      <div className="glass-card mb-8 p-8 relative overflow-hidden group">
        <div className="flex justify-between items-center mb-10 relative z-10">
          <h3 className="text-xl font-bold text-white tracking-wide">Weekly Trajectory</h3>
          <div className="bg-white/5 border border-white/10 rounded-lg px-4 py-1.5 text-sm font-semibold text-secondary">
            Last 7 Days
          </div>
        </div>
        
        <div className="h-[400px] w-full relative z-10">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={weeklyData} margin={{ top: 10, right: 30, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00f2fe" stopOpacity={0.6}/>
                  <stop offset="95%" stopColor="#00f2fe" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis 
                dataKey="name" 
                stroke="#6b7280" 
                tick={{fill: '#9ca3af', fontSize: 13, fontWeight: 500}} 
                axisLine={false} 
                tickLine={false} 
                tickMargin={12}
              />
              <YAxis 
                stroke="#6b7280" 
                tick={{fill: '#9ca3af', fontSize: 13, fontWeight: 500}} 
                axisLine={false} 
                tickLine={false} 
                domain={[0, 100]} 
                tickFormatter={(val) => `${val}%`}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(9, 9, 11, 0.95)', 
                  backdropFilter: 'blur(16px)', 
                  border: '1px solid rgba(255,255,255,0.1)', 
                  borderRadius: '12px', 
                  color: '#fff',
                  boxShadow: '0 10px 25px rgba(0,0,0,0.5)'
                }}
                itemStyle={{ color: '#00f2fe', fontWeight: 'bold' }}
                cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 2 }}
              />
              <Area 
                type="monotone" 
                dataKey="score" 
                stroke="#00f2fe" 
                strokeWidth={4} 
                fillOpacity={1} 
                fill="url(#colorScore)" 
                activeDot={{ r: 8, fill: '#00f2fe', stroke: '#fff', strokeWidth: 3 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-secondary/5 blur-[120px] rounded-full group-hover:bg-secondary/10 transition-colors duration-1000 pointer-events-none" />
      </div>
    </motion.div>
  );
}
