import { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Tracker } from './pages/Tracker';
import { Analytics } from './pages/Analytics';
import { Settings } from './pages/Settings';
import { useNeuroData, getTodayStr } from './hooks/useNeuroData';
import { AnimatePresence } from 'framer-motion';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const neuro = useNeuroData();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Initialize today's data structure
    neuro.initDayIfMissing(getTodayStr());
    setIsLoaded(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!isLoaded) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-background">
        <div className="w-12 h-12 rounded-full border-4 border-white/10 border-t-primary animate-spin shadow-[0_0_30px_rgba(0,242,254,0.3)]" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 ml-64 p-12 min-h-screen relative overflow-hidden">
        {/* Ambient background glow for depth */}
        <div className="fixed top-0 right-0 w-[800px] h-[800px] bg-primary/10 blur-[150px] rounded-full pointer-events-none -z-10 animate-pulse transition-all duration-1000" />
        <div className="fixed bottom-0 left-64 w-[600px] h-[600px] bg-accent/5 blur-[120px] rounded-full pointer-events-none -z-10" />

        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && <Dashboard key="dashboard" neuro={neuro} />}
          {activeTab === 'tracker' && <Tracker key="tracker" neuro={neuro} />}
          {activeTab === 'analytics' && <Analytics key="analytics" neuro={neuro} />}
          {activeTab === 'settings' && <Settings key="settings" />}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
