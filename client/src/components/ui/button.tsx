export const Button = ({ children, className, disabled, onClick }: any) => (
  <button className={className} disabled={disabled} onClick={onClick}>{children}</button>
);
