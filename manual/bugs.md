# Defects (Part 1)

> DRAFT from the screenshots of 10.10.2026. Reproduce each defect 2-3 times on a clean install
> and fix the steps if needed before submitting. Keep at most two.

## BUG-1: Consent error stays visible after the checkbox "Я согласен на обработку персональных данных" is ticked

- **Environment:** Android Studio emulator Pixel 6a, Android 13 (API 33), my moldcell <version>
- **Preconditions:** Clean install; language "Русский" selected; registration "С электронной почтой" opened
- **Steps to reproduce:**
  1. Enter a valid e-mail (disposable address) in the first field.
  2. Enter a password that satisfies all rules and the same password in "Подтвердите пароль".
  3. Leave the consent checkbox unchecked: the error "Для продолжения необходимо согласие на обработку данных." appears.
  4. Tick the consent checkbox.
- **Actual result:** The checkbox is ticked, but the error text is still displayed.
- **Expected result:** The error disappears as soon as consent is given.
- **Severity:** Minor
- **Priority:** Low
- **Evidence:** `manual/evidence/` (screenshots 13:58, before and after ticking). Do not publish a password you use elsewhere.

## BUG-2 (optional, confirm first): Password strength meter rates a keyboard-row password as acceptable

- **Preconditions:** Same registration form
- **Steps:** Enter the password `asdfghjkl` and look at the strength indicator.
- **Actual result:** "Средний - приемлемый пароль" with two of three segments filled, the same level as a password meeting all five rules ("Asdfghj1!"); the third segment was not filled for any tested password.
- **Expected result:** A well-known keyboard sequence is rated weak, and a password meeting all rules rates higher than one that misses two.
- **Severity:** Minor
- **Priority:** Low
- Alternative: report this as the "product risk" instead of a defect if the product team's rule is only length/character classes.

---

## If a defect cannot be reproduced: product risk
- **Risk:** ...
- **How to verify:** ...
