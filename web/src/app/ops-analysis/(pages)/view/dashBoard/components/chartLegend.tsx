import React, { useState, useRef, useEffect } from 'react';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { randomColorForLegend } from '@/app/ops-analysis/utils/randomColorForChart';

interface LegendItem {
  name: string;
  [key: string]: any;
}

interface ChartLegendProps {
  chart?: any;
  data: LegendItem[];
  colors?: string[];
  selected?: Record<string, boolean>;
  onToggleSelect?: (name: string) => void;
}

const ChartLegend: React.FC<ChartLegendProps> = ({
  chart,
  data = [],
  colors = randomColorForLegend(),
  selected = {},
  onToggleSelect,
}) => {
  const [internalSelected, setInternalSelected] = useState<
    Record<string, boolean>
  >({});
  const legendScrollWrapRef = useRef<HTMLUListElement>(null);

  const finalSelected =
    Object.keys(selected).length > 0 ? selected : internalSelected;

  useEffect(() => {
    if (!chart) return;

    const handleLegendSelectChanged = (info: any) => {
      setInternalSelected(info.selected);
    };

    chart.on('legendselectchanged', handleLegendSelectChanged);

    return () => {
      chart.off('legendselectchanged', handleLegendSelectChanged);
    };
  }, [chart]);

  useEffect(() => {
    const newSelected: Record<string, boolean> = {};
    data.forEach((item) => {
      newSelected[item.name] = !['max', 'MAX'].includes(item.name);
    });
    setInternalSelected(newSelected);
  }, [data]);

  const handleToggleSelect = (name: string) => {
    if (onToggleSelect) {
      onToggleSelect(name);
    } else {
      dispatchAction('legendToggleSelect', name);
    }
  };

  const mouseDownplay = () => {
    dispatchAction('downplay');
    dispatchAction('hideTip');
  };

  const mouseOver = (item: LegendItem) => {
    mouseDownplay();
    dispatchAction('highlight', item.name);
    dispatchAction('showTip', item.name, { seriesIndex: 0 });
  };

  const dispatchAction = (type: string, name?: string, config = {}) => {
    if (chart) {
      chart.dispatchAction({
        type: type,
        name: name,
        ...config,
      });
    }
  };

  return (
    <div className="h-full z-10">
      <div className="h-full flex flex-col">
        <ul
          ref={legendScrollWrapRef}
          className="flex-1 flex flex-col overflow-y-auto"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          onMouseLeave={mouseDownplay}
        >
          {data.map((item, index) => (
            <li
              key={index}
              className={`
                cursor-pointer flex items-center w-full py-1.5 px-2
                ${index % 2 === 1 ? 'bg-[var(--color-bg-2)]' : 'bg-[var(--color-bg-4)]'}
                ${!finalSelected[item.name] ? 'opacity-40' : ''}
                hover:bg-[var(--color-bg-3)]
              `}
              onMouseOver={() => mouseOver(item)}
              onClick={() => handleToggleSelect(item.name)}
            >
              <div
                className="inline-block w-4 h-1 rounded-sm flex-shrink-0 self-center"
                style={{
                  backgroundColor: finalSelected[item.name]
                    ? colors[index % colors.length]
                    : 'var(--color-text-4)',
                }}
              />
              <div
                className={`
                  text-xs leading-4 inline-block pl-1.5
                  ${finalSelected[item.name] ? 'text-[var(--color-text-2)]' : 'text-[var(--color-text-4)]'}
                `}
              >
                <EllipsisWithTooltip
                  className="max-w-[120px] whitespace-nowrap overflow-hidden text-ellipsis"
                  text={item.name || '--'}
                />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChartLegend;
