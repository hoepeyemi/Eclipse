"use client";

import React from 'react';
import DymensionInterface from '@/components/DymensionInterface';
import { Toaster } from 'sonner';

export default function DymensionPage() {
  return (
    <main className="container mx-auto py-6">
      <div className="mb-8 space-y-4">
        <h1 className="text-3xl font-bold">Dymension RollApp CLI</h1>
        <p className="text-muted-foreground">
          Create and manage RollApps on the Dymension network using natural language commands. 
          Supports environment setup, RollApp creation, sequencer operations, relayer configuration, 
          eIBC client setup, full node deployment, and block explorer integration.
        </p>
      </div>
      <DymensionInterface />
      <Toaster />
    </main>
  );
} 