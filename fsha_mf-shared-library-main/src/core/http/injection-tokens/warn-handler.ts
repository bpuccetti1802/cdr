import { HttpContextToken } from '@angular/common/http';

export const SHOULD_SKIP_WARN_HANDLER = new HttpContextToken<boolean>(() => false);
