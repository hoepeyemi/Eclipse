"use client";

import React, { useState, useRef } from 'react';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Code, Terminal } from 'lucide-react';
import { toast } from 'sonner';
import LoadingSpinner from './LoadingSpinner';
import { Badge } from './ui/badge';
import CommandDocs from './ui/command-docs';

export interface Command {
  name: string;
  description: string;
  example: string;
  category: string; // Required field
}

interface CommandResult {
  status: string;
  output: string;
  raw_output?: any;
  error?: string;
}

const DymensionInterface: React.FC = () => {
  const [command, setCommand] = useState('');
  const [loading, setLoading] = useState(false);
  const [commandHistory, setCommandHistory] = useState<{cmd: string, result: CommandResult}[]>([]);
  const [commandSuggestions, setCommandSuggestions] = useState<Command[]>([]);
  const [activeTab, setActiveTab] = useState<string>('command');
  const commandInputRef = useRef<HTMLInputElement>(null);
  
  const fetchCommandSuggestions = async () => {
    try {
      const response = await fetch('/api/dymension/help');
      if (!response.ok) {
        throw new Error('Failed to fetch command suggestions');
      }
      const data = await response.json();
      if (data.status === 'success' && Array.isArray(data.commands)) {
        const processedCommands = data.commands.map((cmd: Partial<Command>) => ({
          ...cmd,
          category: cmd.category || 'General',
        })) as Command[];
        setCommandSuggestions(processedCommands);
      }
    } catch (error) {
      console.error('Error fetching command suggestions:', error);
      toast.error('Failed to load command suggestions');
    }
  };

  React.useEffect(() => {
    fetchCommandSuggestions();
  }, []);

  const executeCommand = async () => {
    if (!command.trim()) {
      toast.error('Please enter a command');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/dymension/command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
      });

      if (!response.ok) {
        throw new Error('Failed to execute command');
      }

      const result = await response.json();
      setCommandHistory(prev => [...prev, { cmd: command, result }]);
      setCommand('');
      
      if (result.status === 'success') {
        toast.success('Command executed successfully');
      } else if (result.error) {
        toast.error(result.error);
      }
      
      setActiveTab('history');
    } catch (error) {
      console.error('Error executing command:', error);
      toast.error('Failed to execute command');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      executeCommand();
    }
  };

  const applyExample = (example: string) => {
    setCommand(example);
    if (commandInputRef.current) {
      commandInputRef.current.focus();
    }
  };

  return (
    <Card className="w-full max-w-5xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center">
          <Terminal className="h-6 w-6 mr-2" />
          Dymension RollApp CLI
        </CardTitle>
        <CardDescription>
          Create and manage your RollApps on Dymension using natural language commands
        </CardDescription>
      </CardHeader>
      
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid grid-cols-3 mx-4">
          <TabsTrigger value="command">Command</TabsTrigger>
          <TabsTrigger value="docs">Documentation</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>
        
        <CardContent>
          <TabsContent value="command" className="space-y-4 pt-2">
            <div className="flex space-x-2">
              <Input
                ref={commandInputRef}
                placeholder="Enter your command in natural language (e.g., 'Create a new wallet named mywallet')"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                className="flex-1"
              />
              <Button 
                onClick={executeCommand} 
                disabled={loading || !command.trim()}
                className="min-w-[100px]"
              >
                {loading ? <LoadingSpinner size="sm" /> : "Execute"}
              </Button>
            </div>
            
            <Alert>
              <Code className="h-4 w-4" />
              <AlertTitle>Command Examples</AlertTitle>
              <AlertDescription>
                Use the Documentation tab to view all available commands and examples.
              </AlertDescription>
            </Alert>
          </TabsContent>
          
          <TabsContent value="docs" className="pt-2">
            <ScrollArea className="h-[500px] pr-4">
              <div className="space-y-4">
                <h3 className="text-lg font-medium mb-2">Dymension CLI Commands</h3>
                {commandSuggestions.length > 0 ? (
                  <CommandDocs commands={commandSuggestions} onUseExample={applyExample} />
                ) : (
                  <div className="flex items-center justify-center h-20">
                    <LoadingSpinner />
                  </div>
                )}
              </div>
            </ScrollArea>
          </TabsContent>
          
          <TabsContent value="history" className="pt-2">
            <ScrollArea className="h-[500px] pr-4">
              {commandHistory.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-20 text-muted-foreground">
                  <p>No commands executed yet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {commandHistory.map((item, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="font-mono bg-muted px-2 py-1 rounded text-sm break-all">
                          {item.cmd}
                        </span>
                        <Badge 
                          variant={item.result.status === 'success' ? 'default' : 'destructive'} 
                          className="ml-auto"
                        >
                          {item.result.status}
                        </Badge>
                      </div>
                      
                      {item.result.error ? (
                        <Alert variant="destructive" className="mt-2">
                          <AlertTitle>Error</AlertTitle>
                          <AlertDescription>
                            {item.result.error}
                          </AlertDescription>
                        </Alert>
                      ) : null}
                      
                      {item.result.output ? (
                        <div className="bg-muted p-3 rounded-md mt-2 overflow-x-auto">
                          <pre className="text-sm whitespace-pre-wrap">
                            {typeof item.result.output === 'string' 
                              ? item.result.output 
                              : JSON.stringify(item.result.output, null, 2)
                            }
                          </pre>
                        </div>
                      ) : null}
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </TabsContent>
        </CardContent>
      </Tabs>
      
      <CardFooter className="flex justify-between">
        <p className="text-sm text-muted-foreground">
          Powered by Dymension RollApp SDK
        </p>
      </CardFooter>
    </Card>
  );
};

export default DymensionInterface;