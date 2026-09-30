import { HttpContextToken } from '@angular/common/http';

export const SHOULD_SKIP_TOKEN_HANDLER = new HttpContextToken<boolean>(() => true);
