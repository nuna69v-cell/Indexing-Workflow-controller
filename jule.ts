import { Command } from 'commander';
import chalk from 'chalk';
import { execSync } from 'child_process';

const program = new Command();

program
  .name('jule')
  .description('Jule CLI - GenX VisionOps Infrastructure Manager')
  .version('1.0.0');

program
  .command('setup')
  .description('Setup the GenX VisionOps environment')
  .action(() => {
    console.log(chalk.blue('Setting up GenX VisionOps...'));
    try {
      execSync('./setup.sh', { stdio: 'inherit' });
      console.log(chalk.green('Setup complete.'));
    } catch (error) {
      console.error(chalk.red('Setup failed.'));
    }
  });

program
  .command('start')
  .description('Start the GenX VisionOps network')
  .action(() => {
    console.log(chalk.blue('Starting GenX VisionOps...'));
    try {
      execSync('./start.sh', { stdio: 'inherit' });
    } catch (error) {
      console.error(chalk.red('Failed to start network.'));
    }
  });

program
  .command('deploy')
  .description('Deploy continuously via PM2')
  .action(() => {
    console.log(chalk.blue('Deploying continuously...'));
    try {
      execSync('./jules-deploy.sh', { stdio: 'inherit' });
    } catch (error) {
      console.error(chalk.red('Deployment failed.'));
    }
  });

program
  .command('status')
  .description('Check system status')
  .action(() => {
    console.log(chalk.blue('Checking system status...'));
    try {
      const status = execSync('pm2 status', { encoding: 'utf8' });
      console.log(status);
    } catch (error) {
      console.log(chalk.yellow('PM2 not running or no processes found.'));
    }
  });

program.parse(process.argv);
