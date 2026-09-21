# Privacy Policy — Image Randomizer FA

**Effective date:** September 21, 2026  
**Last updated:** September 21, 2026

Image Randomizer FA is a personal, non-commercial Windows desktop application for generating visual-reference collages from image sources selected by the user. The application is developed as an open-source local application.

This Privacy Policy explains how Image Randomizer FA handles information when you use its local features and, when available, choose to connect your Pinterest account through Pinterest's official OAuth authorization flow.

## Summary

- The app runs locally on your computer.
- Local reference images remain in folders selected by you and are not uploaded by the app.
- The Pinterest integration is intended only for Pinterest data that you explicitly authorize through OAuth.
- Pinterest API data is used only to provide the reference-selection feature during the active app session.
- Pinterest API data, including board and Pin lists, is not persistently stored on disk.
- The app does not sell, rent, share, or use personal data for advertising, analytics, profiling, or AI/ML training.
- There is no developer-operated backend server or third-party data broker.

## Local application data

### Local image folders

You may select folders on your device as image sources. The app reads supported image files from active folders to build a local random-reference pool.

Your local image files are not copied, uploaded, transmitted, or made available to the developer. Their paths are used locally only to display selected references in the application.

### Local settings

The app stores limited settings locally on your device, including configured image-folder entries and the selected interface language. These settings remain on your computer and are used only to restore your preferences when the app is opened again.

## Pinterest integration

Pinterest integration is the next planned feature of Image Randomizer FA. If you choose to use it once it is available, the app will use Pinterest's official OAuth authorization flow. The app will not ask for, collect, or store your Pinterest password, session cookies, or login credentials.

### Permissions and data accessed

The integration is intended to request only the Pinterest permissions needed for the feature: reading boards and Pins that belong to, or are available to, the Pinterest account you authorize.

After you authorize the app, it may access:

- Board identifiers and names needed to let you select a board as a reference source.
- Pin identifiers and image URLs needed to select and display authorized Pins as visual references.
- OAuth access and refresh tokens needed to maintain the authorized connection.

The app is not intended to publish Pins, create or edit boards, modify Pinterest content, access Pinterest passwords, or perform actions on your behalf beyond the authorized read-only reference workflow.

### How Pinterest data is used

Pinterest data will be used solely to provide the user-facing visual-reference feature:

1. The app requests authorized board and Pin information from Pinterest when it is needed for the current session.
2. Authorized Pins may be included in the same random-reference pool as local images.
3. When a Pinterest Pin is selected for display, its image is loaded from Pinterest's image service on demand and displayed in the app.

The app does not use Pinterest data for advertising, behavioral profiling, analytics, resale, audience building, or AI/ML training.

### Storage and retention

Image Randomizer FA is designed not to persist Pinterest API content.

- Board data, Pin data, Pin identifiers, image URLs, and decoded Pinterest images are kept in memory only while the app is running.
- This transient in-memory data is discarded when the application closes.
- The app calls the Pinterest API again when information is needed in a later session rather than maintaining a disk cache of Pinterest API data.
- Pinterest images are not downloaded as permanent image files by the app.

OAuth access and refresh tokens are treated separately from Pinterest content. They are stored locally on the user's device only to maintain the authorized connection between sessions. They are not uploaded to a developer-operated server, committed to the public source repository, sold, or shared with third parties.

## Sharing and disclosures

Image Randomizer FA does not operate a backend service and does not sell, rent, trade, or disclose user data to third parties.

When Pinterest integration is used, communication takes place directly between your device and Pinterest's services as required to complete OAuth authorization and API requests. Pinterest's handling of information is governed by its own policies and terms.

## Revoking access and deleting local data

You can stop using the Pinterest integration at any time.

- You may revoke the app's authorization through the authorized-applications settings in your Pinterest account.
- You may delete the app's locally stored Pinterest token file to remove the saved local connection.
- You may delete the app's local settings files to remove saved folder configuration and language preferences.
- Closing the app clears its in-memory Pinterest board, Pin, URL, and image data.

Revoking access prevents the app from obtaining or refreshing authorization for future Pinterest API requests.

## Security

The app uses Pinterest's official OAuth authorization flow rather than collecting Pinterest credentials. Tokens are intended to remain on the local device and are excluded from the public repository through version-control rules.

No system can guarantee absolute security. You are responsible for keeping access to your device and local application-data folder secure.

## Children

Image Randomizer FA is not directed to children. The developer does not knowingly collect personal information from children.

## Changes to this policy

This policy may be updated when the application changes, particularly when the Pinterest integration is implemented or its data handling changes. The effective date at the top of this document will be updated when material changes are made.

## Contact

For questions about this Privacy Policy or Image Randomizer FA's data practices, please open an issue in the project's public GitHub repository.

## Open-source transparency

The source code for Image Randomizer FA is publicly available in its GitHub repository. The repository is intended to make the app's local storage, OAuth, and Pinterest API handling reviewable.
