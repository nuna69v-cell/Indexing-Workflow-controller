import { motion } from "framer-motion";
import { 
  Terminal, 
  Zap, 
  Target, 
  Settings, 
  Laptop, 
  Github, 
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  MonitorDot
} from "lucide-react";
import { Navbar } from "@/components/Navbar";

const GITHUB_URL = "https://github.com/nuna69v-cell/all-in-one-desktop-mode-";

export default function Home() {
  const fadeInUp = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
  };

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] opacity-20 pointer-events-none blur-[120px] bg-gradient-to-b from-cyan-500/40 via-blue-600/20 to-transparent rounded-full -z-10" />
      
      <Navbar />

      <main>
        {/* HERO SECTION */}
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col items-center text-center">
          {/* Decorative badge */}
          <motion.a 
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm font-medium text-cyan-400 hover:bg-white/10 transition-colors mb-8 backdrop-blur-md"
          >
            <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
            v1.0 is now available open-source
            <ArrowRight className="w-4 h-4 ml-1" />
          </motion.a>

          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-5xl sm:text-6xl md:text-8xl font-display font-extrabold tracking-tight mb-8 max-w-5xl text-gradient leading-[1.1]"
          >
            The ultimate <span className="text-gradient-primary">workspace</span> for deep work.
          </motion.h1>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="text-lg md:text-xl text-muted-foreground mb-12 max-w-2xl leading-relaxed"
          >
            All-in-One Desktop Mode transforms your operating system into a hyper-focused, distraction-free environment tailored for maximum productivity.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto"
          >
            <a 
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl text-base font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-[0_0_30px_rgba(0,180,255,0.3)] hover:shadow-[0_0_50px_rgba(0,180,255,0.5)] hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2"
            >
              Download Now
              <ChevronRight className="w-5 h-5" />
            </a>
            <a 
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl text-base font-semibold bg-white/5 text-white border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all duration-300 flex items-center justify-center gap-2 backdrop-blur-sm"
            >
              <Github className="w-5 h-5" />
              View on GitHub
            </a>
          </motion.div>

          {/* Hero Image / Mockup */}
          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.5 }}
            className="mt-20 w-full max-w-5xl relative rounded-2xl md:rounded-[2rem] overflow-hidden border border-white/10 shadow-2xl shadow-black/50 glass-panel"
          >
            <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent z-10 pointer-events-none" />
            <img 
              src={`${import.meta.env.BASE_URL}images/product-mockup.png`} 
              alt="Desktop Mode Interface" 
              className="w-full h-auto object-cover transform hover:scale-[1.02] transition-transform duration-700"
            />
          </motion.div>
        </section>

        {/* FEATURES SECTION */}
        <section id="features" className="py-24 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={fadeInUp}
              className="text-center mb-20"
            >
              <h2 className="text-3xl md:text-5xl font-display font-bold mb-6">Everything you need.<br/>Nothing you don't.</h2>
              <p className="text-muted-foreground text-lg max-w-2xl mx-auto">Engineered from the ground up to eliminate context switching and keep you in the zone.</p>
            </motion.div>

            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={staggerContainer}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8"
            >
              {[
                { icon: Terminal, title: "All-in-One Workspace", desc: "Consolidate your tools into a single, unified interface that strips away OS clutter." },
                { icon: Zap, title: "Desktop Optimization", desc: "Lightweight resource footprint ensures zero latency and maximum battery life." },
                { icon: Target, title: "Productivity Tools", desc: "Built-in pomodoro timers, task lists, and focus analytics right at your fingertips." },
                { icon: Settings, title: "Highly Customizable", desc: "Tweak every pixel and shortcut. Make the environment adapt to your workflow." },
                { icon: Laptop, title: "Cross-Platform", desc: "Consistent experience whether you're working on Windows, macOS, or Linux." },
                { icon: Github, title: "100% Open Source", desc: "Free forever. Inspect the code, contribute features, and build your own plugins." }
              ].map((feature, i) => (
                <motion.div 
                  key={i}
                  variants={fadeInUp}
                  className="group p-8 rounded-3xl bg-card border border-white/5 hover:border-cyan-500/30 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/5 relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-10 transition-opacity duration-500 pointer-events-none">
                    <feature.icon className="w-32 h-32 text-cyan-400" />
                  </div>
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500/10 to-blue-600/10 border border-cyan-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="w-7 h-7 text-cyan-400" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.desc}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="how-it-works" className="py-24 bg-card/30 border-y border-white/5 relative">
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-64 h-64 bg-blue-600/20 rounded-full blur-[100px] -z-10" />
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={fadeInUp}
              className="mb-16"
            >
              <h2 className="text-3xl md:text-5xl font-display font-bold mb-6">Setup in seconds.</h2>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
              {/* Connecting line for desktop */}
              <div className="hidden md:block absolute top-12 left-[15%] right-[15%] h-[2px] bg-gradient-to-r from-cyan-500/0 via-cyan-500/50 to-cyan-500/0" />

              {[
                { step: "01", title: "Download", desc: "Grab the latest release from our GitHub repository for your OS." },
                { step: "02", title: "Configure", desc: "Select your essential apps and set your focus parameters." },
                { step: "03", title: "Engage", desc: "Activate Desktop Mode and watch distractions disappear." }
              ].map((item, i) => (
                <motion.div 
                  key={i}
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true }}
                  variants={{
                    hidden: { opacity: 0, y: 20 },
                    visible: { opacity: 1, y: 0, transition: { delay: i * 0.2, duration: 0.5 } }
                  }}
                  className="relative flex flex-col items-center text-center"
                >
                  <div className="w-24 h-24 rounded-full bg-background border-4 border-card flex items-center justify-center text-2xl font-display font-bold text-cyan-400 shadow-[0_0_30px_rgba(0,180,255,0.15)] mb-8 z-10">
                    {item.step}
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">{item.title}</h3>
                  <p className="text-muted-foreground">{item.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* TESTIMONIALS */}
        <section id="testimonials" className="py-32 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeInUp}
              className="text-center mb-20"
            >
              <h2 className="text-3xl md:text-5xl font-display font-bold mb-6">Loved by developers.</h2>
            </motion.div>

            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={staggerContainer}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            >
              {[
                { quote: "It literally feels like putting blinders on my operating system. My deep work sessions have doubled in length.", author: "Alex K.", role: "Full-stack Engineer" },
                { quote: "The fact that this is open source is mind-blowing. It's cleaner and faster than paid alternatives I've tried.", author: "Sarah M.", role: "Product Designer" },
                { quote: "Finally, a tool that understands that closing Discord isn't enough. It creates an actual boundary for work.", author: "James T.", role: "Indie Hacker" }
              ].map((test, i) => (
                <motion.div 
                  key={i}
                  variants={fadeInUp}
                  className="p-8 rounded-3xl glass-panel relative group"
                >
                  <div className="absolute inset-0 bg-gradient-to-b from-cyan-500/5 to-transparent rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  {/* Unsplash placeholder for avatars - using subtle tech/abstract to fit theme rather than faces */}
                  <div className="mb-8">
                    <svg className="w-10 h-10 text-cyan-500/50" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                    </svg>
                  </div>
                  <p className="text-lg text-white/90 mb-8 leading-relaxed">"{test.quote}"</p>
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg">
                      {test.author.charAt(0)}
                    </div>
                    <div>
                      <h4 className="font-bold text-white">{test.author}</h4>
                      <p className="text-sm text-cyan-400">{test.role}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* BOTTOM CTA */}
        <section className="py-32 relative overflow-hidden">
          {/* Using the AI generated background image here */}
          <div className="absolute inset-0 z-0">
            <img 
              src={`${import.meta.env.BASE_URL}images/hero-bg.png`} 
              alt="Abstract background" 
              className="w-full h-full object-cover opacity-30"
            />
            <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" />
          </div>

          <div className="max-w-4xl mx-auto px-4 relative z-10 text-center">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeInUp}
              className="p-12 md:p-20 rounded-[3rem] glass-panel border-cyan-500/20 bg-background/60"
            >
              <h2 className="text-4xl md:text-6xl font-display font-bold mb-6 text-white">Ready to reclaim your focus?</h2>
              <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
                Join developers worldwide who are using Desktop Mode to ship faster and better. Free and open source.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a 
                  href={GITHUB_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full sm:w-auto px-10 py-5 rounded-2xl text-lg font-bold bg-white text-black shadow-[0_0_40px_rgba(255,255,255,0.2)] hover:shadow-[0_0_60px_rgba(255,255,255,0.3)] hover:scale-105 transition-all duration-300"
                >
                  Download Free
                </a>
                <a 
                  href={GITHUB_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full sm:w-auto px-10 py-5 rounded-2xl text-lg font-bold bg-white/5 text-white border border-white/10 hover:bg-white/10 transition-all duration-300 flex items-center justify-center gap-3"
                >
                  <Github className="w-6 h-6" />
                  Star Repository
                </a>
              </div>
              
              <div className="mt-10 flex flex-wrap justify-center gap-6 text-sm text-muted-foreground font-medium">
                <span className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-cyan-400" /> Open Source</span>
                <span className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-cyan-400" /> Windows / macOS / Linux</span>
                <span className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-cyan-400" /> No Telemetry</span>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="bg-background border-t border-white/5 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <MonitorDot className="w-6 h-6 text-cyan-500" />
            <span className="font-display font-bold text-lg text-white">DesktopMode</span>
          </div>
          
          <p className="text-muted-foreground text-sm text-center md:text-left">
            Built by <a href="https://github.com/nuna69v-cell" target="_blank" rel="noreferrer" className="text-white hover:text-cyan-400 transition-colors">nuna69v-cell</a>. Open source under MIT License.
          </p>
          
          <div className="flex items-center gap-6">
            <a href={GITHUB_URL} target="_blank" rel="noreferrer" className="text-muted-foreground hover:text-white transition-colors">
              <Github className="w-5 h-5" />
              <span className="sr-only">GitHub</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
