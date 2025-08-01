import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import styles from './index.module.scss';
import { useTranslation } from '@/utils/i18n';

interface Task {
  id: number;
  task_name: string;
  train_progress: number;
  is_qa_task: boolean;
}

interface TaskProgressProps {
  activeTabKey?: string;
}

const TaskProgress: React.FC<TaskProgressProps> = ({ activeTabKey }) => {
  const { t } = useTranslation();
  const [tasks, setTasks] = useState<Task[]>([]);
  const { fetchMyTasks } = useKnowledgeApi();
  const searchParams = useSearchParams();
  const id = searchParams ? searchParams.get('id') : null;

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const params = {
          knowledge_base_id: id
        };
        const data = await fetchMyTasks(params);
        setTasks(data);
      } catch (error) {
        console.error(`${t('common.fetchFailed')}: ${error}`);
      }
    };

    fetchTasks();
    const interval = setInterval(fetchTasks, 10000);
    return () => clearInterval(interval);
  }, []);

  // Filter tasks based on activeTabKey
  const filteredTasks = tasks.filter((task) => {
    // Only show tasks for source_files and qa_pairs tabs
    if (!activeTabKey || (activeTabKey !== 'source_files' && activeTabKey !== 'qa_pairs')) {
      return false;
    }

    // For source_files tab, show tasks where is_qa_task is false
    if (activeTabKey === 'source_files') {
      return !task.is_qa_task;
    }

    // For qa_pairs tab, show tasks where is_qa_task is true
    if (activeTabKey === 'qa_pairs') {
      return task.is_qa_task;
    }

    return false;
  });

  // Don't render if no filtered tasks
  if (filteredTasks.length === 0) {
    return null;
  }

  return (
    <div className="p-4 absolute bottom-10 left-0 w-full max-h-[300px] overflow-y-auto">
      {filteredTasks.map((task) => (
        <div key={task.id} className="mb-2">
          <div className="flex justify-between items-center text-xs mb-1">
            <span className="flex-1 truncate" title={task.task_name}>
              {task.task_name}
            </span>
            <span className="ml-2 flex-shrink-0">{task.train_progress}</span>
          </div>
          <div className={`w-full h-2 rounded relative overflow-hidden ${styles.progressContainer}`}>
            <div className={`${styles.progressBar} h-full w-full`}></div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskProgress;
