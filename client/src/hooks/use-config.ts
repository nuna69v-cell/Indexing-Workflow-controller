export const useConfig = () => ({});
export const useBotStatus = () => ({
  data: { is_running: false, last_run: null, next_job: null },
  isLoading: false,
  refetch: () => {}
});
export const useRunJob = () => ({ mutate: (arg?: any) => { console.log(arg); }, isPending: false });
