# Checklist (Part 1)

Environment: Android Studio emulator Pixel 6a, Android 13 (API 33), my moldcell <version: ...>,
Russian UI. Flow under test: language screen -> login screen -> registration (with e-mail) -> OTP.

> Results marked "(screenshot)" come from the screenshots taken on 10.10.2026; re-confirm them
> on a clean install before submitting. "Not run" means not executed yet: run the High ones first.

| # | Check | Priority | Result | Comment |
|---|-------|----------|--------|---------|
| 1 | App starts and the language screen shows 3 languages and Continue | High | Passed | Also covered by the automated test |
| 2 | After language + Continue the login screen opens (username, password, Войти, Забыли пароль?, Регистрация) | High | Passed | Screenshot 11:28; also covered by the automated positive test |
| 3 | Registration: text that is not an e-mail ("mol") shows an inline error | High | Passed | "Ваше имя пользователя должно быть адресом электронной почты." (screenshot 13:53) |
| 4 | Registration: e-mail with a comma instead of a dot is rejected; corrected e-mail clears the error | High | Passed | (screenshot 13:54) |
| 5 | Password rules (8 chars, lower, upper, digit, no username) update live while typing | High | Passed | (screenshot 13:54-13:56) |
| 6 | Password strength meter reflects password quality | Medium | Not run | Observed: "asdfghjkl" is "Средний" (keyboard row), same level as "Asdfghj1!". Decide if this is a defect |
| 7 | Mismatching / matching confirm password: message "Пароли должны совпадать" | Medium | Passed | Matching case shown (screenshot 13:58); check the mismatch case |
| 8 | Consent checkbox: error appears when unchecked and DISAPPEARS after checking | High | Failed | Error text stays after the box is ticked (screenshot 13:58). See BUG-1 |
| 9 | No network on the login / registration screens: clear message, no crash | High | Not run | Mandatory direction |
| 10 | Network lost and restored during registration: the app recovers | Medium | Not run | |
| 11 | Back arrow in the registration form: entered data kept or cleared (note which) | Medium | Not run | Mandatory direction |
| 12 | Empty login form: touching the fields / tapping Войти shows "Пожалуйста, введите имя пользователя.", user stays on the login screen | High | Not run | Covered by the automated negative test. The message is NOT shown on a clean screen (11:28): it appears after interaction |
| 13 | OTP screen: 6 input boxes show "*" placeholders that look like entered characters | Low | Not run | Usability |
| 14 | Accessibility: small grey helper text, contrast, touch targets, font scale 200% | Low | Not run | Usability/accessibility direction |
| 15 | Login with a wrong password / non-existent account is rejected, the user stays on the login screen | High | Not run | Note the exact error text and how long the response takes; also covered by an automated test |

## Prioritization rationale
The entry flow and input validation are used by every new user, so they come first. Network
failures and navigation are common sources of defects. Operations with side effects (finishing a
registration, choosing "С новым номером", payments, tariff changes) are intentionally out of scope.
