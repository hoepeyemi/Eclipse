import Link from 'next/link';
import { ArrowRight, ChartLine, Brain, Zap, TrendingUp, BarChart4, BarChart3, Code, LineChart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export default function HomePage() {
  return (
    <main className="container mx-auto py-12">
      <section className="mb-16 text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-4">
          <span className="text-gradient">Tradi Platform</span>
        </h1>
        <p className="text-xl max-w-3xl mx-auto text-muted-foreground">
          Blockchain development and analysis tools to build and manage your decentralized applications
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <Card className="glass">
          <CardHeader>
            <CardTitle className="flex items-center">
              <LineChart className="h-5 w-5 mr-2" />
              Technical Analysis
            </CardTitle>
            <CardDescription>
              Analyze market data with advanced technical indicators
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Our advanced analysis tools provide insights into market trends and patterns using technical indicators 
              like moving averages, RSI, and more.
            </p>
          </CardContent>
          <CardFooter>
            <Link href="/analyze" className="w-full">
              <Button variant="default" className="w-full">
                <span>Try Analysis</span>
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </Link>
          </CardFooter>
        </Card>

        <Card className="glass">
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="h-5 w-5 mr-2" />
              Price Predictions
            </CardTitle>
            <CardDescription>
              AI-powered price predictions for multiple time horizons
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Get AI-generated price forecasts for various assets across different timeframes, 
              from short-term to long-term outlooks.
            </p>
          </CardContent>
          <CardFooter>
            <Link href="/predict" className="w-full">
              <Button variant="default" className="w-full">
                <span>View Predictions</span>
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </Link>
          </CardFooter>
        </Card>

        <Card className="glass">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Code className="h-5 w-5 mr-2" />
              Dymension RollApp CLI
            </CardTitle>
            <CardDescription>
              Create and manage RollApps on Dymension network
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Deploy and manage Dymension RollApps with a natural language command interface.
              Create wallets, manage tokens, register sequencers, and more.
            </p>
          </CardContent>
          <CardFooter>
            <Link href="/dymension" className="w-full">
              <Button variant="default" className="w-full">
                <span>Open RollApp CLI</span>
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </Link>
          </CardFooter>
        </Card>
      </section>

      <section className="text-center mb-16">
        <h2 className="text-3xl font-bold mb-4">Built for Blockchain Developers</h2>
        <p className="text-lg max-w-3xl mx-auto text-muted-foreground">
          Whether you're analyzing market data or building decentralized applications,
          our platform provides the tools you need to succeed.
        </p>
      </section>
    </main>
  );
}