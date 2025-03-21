import Link from 'next/link';
import { ArrowRight, Code } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export default function HomePage() {
  return (
    <main className="container mx-auto py-12">
      <section className="mb-16 text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-4">
          <span className="text-gradient">Dymension RollApp Platform</span>
        </h1>
        <p className="text-xl max-w-3xl mx-auto text-muted-foreground">
          Tools to build and manage your Dymension RollApps with a natural language interface
        </p>
      </section>

      <section className="flex justify-center mb-12">
        <Card className="glass max-w-xl w-full">
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
        <h2 className="text-3xl font-bold mb-4">Built for Dymension Developers</h2>
        <p className="text-lg max-w-3xl mx-auto text-muted-foreground">
          Streamline your RollApp development workflow with our intuitive CLI interface.
          Set up, deploy, and manage your RollApps seamlessly.
        </p>
      </section>
    </main>
  );
}