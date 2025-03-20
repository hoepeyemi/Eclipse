import React from 'react';
import { 
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface CommandExample {
  name: string;
  description: string;
  example: string;
  category: string;
}

interface CommandDocsProps {
  commands: CommandExample[];
  onUseExample: (example: string) => void;
}

const CommandDocs: React.FC<CommandDocsProps> = ({ commands, onUseExample }) => {
  // Group commands by category
  const groupedCommands = commands.reduce<Record<string, CommandExample[]>>((acc, command) => {
    const category = command.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(command);
    return acc;
  }, {});

  const categories = {
    'Setup': {
      filter: (cmd: CommandExample) => cmd.category === 'Setup',
      title: 'Environment Setup',
    },
    'Wallet': {
      filter: (cmd: CommandExample) => cmd.category === 'Wallet',
      title: 'Wallet Management',
    },
    'RollApp': {
      filter: (cmd: CommandExample) => cmd.category === 'RollApp',
      title: 'RollApp Management',
    },
    'Sequencer': {
      filter: (cmd: CommandExample) => cmd.category === 'Sequencer',
      title: 'Sequencer Operations',
    },
    'SequencerMgmt': {
      filter: (cmd: CommandExample) => cmd.category === 'SequencerMgmt',
      title: 'Sequencer Management',
    },
    'Relayer': {
      filter: (cmd: CommandExample) => cmd.category === 'Relayer',
      title: 'Relayer Operations',
    },
    'eIBC': {
      filter: (cmd: CommandExample) => cmd.category === 'eIBC',
      title: 'eIBC Client Operations',
    },
    'Node': {
      filter: (cmd: CommandExample) => cmd.category === 'Node',
      title: 'Full Node Operations',
    },
    'Explorer': {
      filter: (cmd: CommandExample) => cmd.category === 'Explorer',
      title: 'Block Explorer',
    },
    'Other': {
      filter: (cmd: CommandExample) => 
        !['Setup', 'Wallet', 'RollApp', 'Sequencer', 'SequencerMgmt', 'Relayer', 'eIBC', 'Node', 'Explorer'].includes(cmd.category),
      title: 'Other Commands',
    },
  };

  return (
    <div className="space-y-4">
      <Accordion type="multiple" className="w-full">
        {Object.entries(categories).map(([key, { filter, title }]) => {
          const filteredCommands = commands.filter(filter);
          if (filteredCommands.length === 0) return null;
          
          return (
            <AccordionItem key={key} value={key.toLowerCase()}>
              <AccordionTrigger>{title}</AccordionTrigger>
              <AccordionContent>
                <div className="space-y-2">
                  {filteredCommands.map((cmd, i) => (
                    <div key={i} className="p-2 rounded-md border">
                      <div className="flex justify-between items-start mb-1">
                        <h4 className="font-medium">{cmd.name}</h4>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => onUseExample(cmd.example)}
                        >
                          Use
                        </Button>
                      </div>
                      <p className="text-sm text-muted-foreground">{cmd.description}</p>
                      <code className="text-xs block mt-2 p-1 bg-muted rounded">{cmd.example}</code>
                    </div>
                  ))}
                </div>
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </div>
  );
};

export default CommandDocs; 