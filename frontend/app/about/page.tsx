export default function AboutPage() {
    return (
      <main className="container mx-auto py-6">
        <h1 className="text-3xl font-bold mb-6">About Dymension RollApp CLI</h1>
        
        <div className="prose prose-stone max-w-none">
          <p>
            The Dymension RollApp CLI is a powerful interface designed to simplify the creation, 
            deployment, and management of Dymension RollApps. With a natural language interface, 
            it makes blockchain development more accessible to developers of all experience levels.
          </p>
          
          <h2>Key Features</h2>
          <ul>
            <li>Natural language command interface for Dymension CLI operations</li>
            <li>Comprehensive toolset for RollApp initialization and configuration</li>
            <li>Sequencer and relayer management capabilities</li>
            <li>Full node deployment and monitoring tools</li>
            <li>Wallet management for Dymension operations</li>
          </ul>
          
          <h2>Technology Stack</h2>
          <p>
            The Dymension RollApp CLI platform is built using modern technologies including Next.js, 
            React, TypeScript, Flask, and integrates with the Dymension network tools. The platform 
            provides a seamless interface to the underlying Roller CLI utilities and Dymension binaries.
          </p>
          
          <h2>About Dymension</h2>
          <p>
            Dymension is a modular blockchain network designed to scale blockchain technology 
            through RollApps (application-specific rollups). The network enables developers to 
            build customized, high-performance decentralized applications with seamless interoperability.
          </p>
        </div>
      </main>
    );
  }