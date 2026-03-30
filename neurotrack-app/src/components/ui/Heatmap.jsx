import React, { useRef, useEffect } from 'react';
import clsx from 'clsx';
import { getTodayStr } from '../../hooks/useNeuroData';

export function Heatmap({ dataHistory }) {
  const containerRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to current day (right)
    if (containerRef.current) {
      containerRef.current.scrollLeft = containerRef.current.scrollWidth;
    }
  }, [dataHistory]);

  const today = new Date();
  const startDate = new Date();
  startDate.setDate(today.getDate() - 364);
  while (startDate.getDay() !== 0) {
    startDate.setDate(startDate.getDate() - 1);
  }

  const weeks = [];
  const monthLabels = [];
  let currentMonth = -1;
  let curDate = new Date(startDate);

  for (let w = 0; w < 53; w++) {
    const week = [];
    let weekMonth = -1;
    for (let d = 0; d < 7; d++) {
      if (curDate > today) {
        week.push(null);
      } else {
        const key = curDate.toISOString().split('T')[0];
        const dayData = dataHistory[key];
        const score = dayData ? dayData.score : 0;
        let level = 0;
        if (score > 0) level = 1;
        if (score >= 40) level = 2;
        if (score >= 70) level = 3;
        if (score >= 90) level = 4;
        week.push({ date: key, score, level });
      }
      if (d === 0) weekMonth = curDate.getMonth();
      curDate.setDate(curDate.getDate() + 1);
    }
    weeks.push(week);
    if (weekMonth !== currentMonth) {
      monthLabels.push({ text: new Date(2000, weekMonth, 1).toLocaleString('en-US', { month: 'short' }), weekIndex: w });
      currentMonth = weekMonth;
    }
  }

  return (
    <div className="flex flex-col gap-1 text-[11px] text-[#8b949e] overflow-x-auto pb-4" ref={containerRef}>
      <div className="grid grid-cols-[repeat(53,12px)] gap-[3px] ml-[30px] mb-1 min-w-max">
        {Array.from({ length: 53 }).map((_, w) => {
          const month = monthLabels.find(m => m.weekIndex === w);
          return (
            <div key={w} className="col-span-1 whitespace-nowrap overflow-visible">
              {month ? month.text : ''}
            </div>
          );
        })}
      </div>

      <div className="flex gap-2 min-w-max">
        <div className="grid grid-rows-[repeat(7,12px)] gap-[3px] text-right w-[22px] leading-[12px]">
          {['', 'Mon', '', 'Wed', '', 'Fri', ''].map((d, i) => (
            <div key={i}>{d}</div>
          ))}
        </div>

        <div className="grid grid-flow-col grid-rows-[repeat(7,12px)] grid-cols-[repeat(53,12px)] gap-[3px]">
          {weeks.map((week, w) => (
            <React.Fragment key={w}>
              {week.map((cell, d) => (
                cell ? (
                  <div
                    key={`${w}-${d}`}
                    className={clsx(
                      "w-[12px] h-[12px] rounded-sm transition-transform duration-200 hover:scale-[1.8] hover:z-20 cursor-crosshair relative",
                      cell.level === 0 && 'bg-[#161b22] hover:shadow-[0_0_8px_rgba(255,255,255,0.2)]',
                      cell.level === 1 && 'bg-[#0e4429] hover:shadow-[0_0_8px_rgba(14,68,41,0.8)]',
                      cell.level === 2 && 'bg-[#006d32] hover:shadow-[0_0_8px_rgba(0,109,50,0.8)]',
                      cell.level === 3 && 'bg-[#26a641] hover:shadow-[0_0_8px_rgba(38,166,65,0.8)]',
                      cell.level === 4 && 'bg-[#39d353] hover:shadow-[0_0_8px_rgba(57,211,83,0.8)]',
                    )}
                    title={`${cell.date}: ${cell.score}% Productivity`}
                  />
                ) : (
                  <div key={`${w}-${d}`} className="w-[12px] h-[12px]" />
                )
              ))}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="flex justify-end items-center mt-2 ml-[30px] min-w-max">
        <div className="flex items-center gap-1">
          <span className="mr-1">Less</span>
          <div className="w-3 h-3 rounded-sm bg-[#161b22]" />
          <div className="w-3 h-3 rounded-sm bg-[#0e4429]" />
          <div className="w-3 h-3 rounded-sm bg-[#006d32]" />
          <div className="w-3 h-3 rounded-sm bg-[#26a641]" />
          <div className="w-3 h-3 rounded-sm bg-[#39d353]" />
          <span className="ml-1">More</span>
        </div>
      </div>
    </div>
  );
}
