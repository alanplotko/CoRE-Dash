# Changelog
All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## Planned Features

- ~~Google Sign-in~~ >> **Added in v0.1.0-alpha**
- Web chat
- Organize, host, and attend events
  - Members can upload their class eschedules to help in event planning
  - Members can list recurring times in which they have commitments to clubs and other activities in which they cannot attend an event
- Upload documents
  - Use Google Drive API to fetch CoRE documents for reading
  - Integrate forms into the application rather than sending links via email
- Send automated emails via the application for CoRE meetings
- Manage member lists via the application
  - Send verification email (via SendGrid?) with token in url (/resend/insert-token-here)

## v0.1.1-alpha / 2015-08-15
- [Bugfix] Fix issue in which unauthorized users did not have their sessions cleared and were redirected to an empty dashboard page
- [Enhancement] Add padding and decrease spacing between lines for multiline error messages

## v0.1.0-alpha / 2015-08-15
- Beginning of documentation via changelog
- [Feature] Google sign-in
