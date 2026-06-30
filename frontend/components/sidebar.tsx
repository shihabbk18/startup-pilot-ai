import {
  BarChart3,
  Bot,
  CreditCard,
  FileText,
  FolderKanban,
  Library,
  Settings,
  Users
} from "lucide-react";

const navItems = [
  ["Projects", FolderKanban],
  ["Recent generations", BarChart3],
  ["Saved reports", FileText],
  ["Document library", Library],
  ["Team members", Users],
  ["AI Chat", Bot],
  ["Settings", Settings],
  ["Billing", CreditCard]
];

export function Sidebar() {
  return (
    <aside className="sticky top-0 hidden h-screen border-r border-border bg-card/80 p-5 backdrop-blur xl:block">
      <div className="mb-8 flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-primary text-sm font-black text-white">
          SP
        </div>
        <div>
          <p className="text-xs font-black uppercase text-accent">StartupPilot AI</p>
          <h1 className="text-lg font-black">Founder OS</h1>
        </div>
      </div>
      <nav className="grid gap-2">
        {navItems.map(([label, Icon]) => (
          <a
            href="#"
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-bold text-muted transition hover:bg-white/5 hover:text-foreground"
            key={label as string}
          >
            <Icon className="h-4 w-4" />
            {label as string}
          </a>
        ))}
      </nav>
    </aside>
  );
}

