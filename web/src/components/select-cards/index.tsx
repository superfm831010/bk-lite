import React from 'react';
import Icon from '@/components/icon';

interface CardItem {
  icon: string;
  title: string;
  content: string;
  value: string;
}

interface SelectCardsProps {
  data: CardItem[];
  value?: string[];
  onChange?: (value: string[]) => void;
  className?: string;
}

const SelectCards: React.FC<SelectCardsProps> = ({
  data = [],
  value = [],
  onChange,
  className = '',
}) => {
  const handleCardClick = (item: CardItem) => {
    const newValue = value.includes(item.value)
      ? value.filter((v) => v !== item.value)
      : [...value, item.value];
    onChange?.(newValue);
  };

  return (
    <div className={`flex flex-wrap gap-4 ${className}`}>
      {data.map((item, index) => (
        <div
          key={index}
          onClick={() => handleCardClick(item)}
          className={`w-[220px] bg-[var(--color-bg-1)] border-2 ${
            value.includes(item.value)
              ? 'border-[var(--color-primary)] shadow-lg'
              : 'border-blue-300'
          } shadow-md hover:shadow-lg transition-all duration-300 ease-in-out rounded-lg p-3 relative cursor-pointer`}
        >
          <div className="flex items-center space-x-4 my-1">
            <Icon type={item.icon} className="text-2xl" />
            <h2 className="text-[16px] font-bold m-0">{item.title}</h2>
          </div>
          <p className="text-[var(--color-text-3)] text-[13px] mt-2">
            {item.content}
          </p>
        </div>
      ))}
    </div>
  );
};

export default SelectCards;
