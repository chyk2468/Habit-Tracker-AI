import { motion, useSpring, useTransform } from 'framer-motion';
import { useEffect } from 'react';
import clsx from 'clsx';

export function StatCard({ title, value, label, icon: Icon, colorClass = 'text-accent', glowClass = 'bg-accent' }) {
  const spring = useSpring(0, { duration: 2000, bounce: 0 });
  const displayValue = useTransform(spring, (current) => Math.round(current));

  useEffect(() => {
    spring.set(value);
  }, [value, spring]);

  return (
    <motion.div 
      whileHover={{ scale: 1.02, y: -4 }}
      className="glass-card flex flex-col justify-between overflow-hidden relative group"
    >
      <div className="flex justify-between items-start mb-4 relative z-10">
        <h4 className="text-gray-400 font-medium text-sm uppercase tracking-wider">{title}</h4>
        {Icon && <Icon size={20} className={clsx(colorClass, "opacity-70 group-hover:opacity-100 transition-opacity")} />}
      </div>
      <div className="relative z-10">
        <div className="flex items-end gap-1">
          <motion.span className="text-4xl font-extrabold tracking-tight text-white">{displayValue}</motion.span>
          {label && <span className="text-lg text-gray-400 font-medium pb-[2px]">{label}</span>}
        </div>
      </div>
      
      {/* Background glow */}
      <div className={clsx(
        "absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-10 pointer-events-none transition-opacity duration-500 group-hover:opacity-30",
        glowClass
      )} />
    </motion.div>
  );
}
