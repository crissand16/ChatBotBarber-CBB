import type { PageHeaderProps } from '../interfaces/PageHeaderInter';

function PageHeader({ eyebrow, title, description, actions }: PageHeaderProps) {
  return (
    <header className="page-header">
      <div className="page-header-text">
        {eyebrow && <span className="page-eyebrow">{eyebrow}</span>}
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>

      {actions && <div className="page-header-actions">{actions}</div>}
    </header>
  );
}

export default PageHeader;
