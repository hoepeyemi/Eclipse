"use client";

import Analyze from "@/components/Analyze";
import { Toaster } from 'sonner';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, Code } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function AnalyzePage() {
  return (
    <main className="container mx-auto py-6">
      <div className="mb-8 space-y-4">
        <h1 className="text-3xl font-bold">Market Analysis</h1>
        <p className="text-muted-foreground">
          Analyze market trends and patterns with technical indicators and insights.
        </p>
      </div>

      <Card className="mb-6 bg-amber-50 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800">
        <CardHeader className="pb-2">
          <CardTitle className="text-amber-800 dark:text-amber-400 flex items-center">
            <Code className="h-5 w-5 mr-2" />
            New Feature: Dymension RollApp CLI
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-amber-700 dark:text-amber-300">
            We've added a new feature to help you create and manage RollApps on the Dymension network. 
            Try out our natural language command interface for Dymension operations!
          </p>
        </CardContent>
        <CardFooter>
          <Link href="/dymension">
            <Button variant="outline" className="text-amber-800 dark:text-amber-400 border-amber-300 dark:border-amber-700 hover:bg-amber-100 dark:hover:bg-amber-900/30">
              Try Dymension CLI
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </CardFooter>
      </Card>
      
      <Analyze />
      <Toaster />
    </main>
  );
}