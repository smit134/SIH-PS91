"""SMS Gateway Integration Service for ThinkForge.

Supports delivering actual SMS OTPs to mobile devices in India via Fast2SMS.
"""

import logging
import re
from typing import Optional
import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def extract_10_digit_phone(phone: str) -> str:
    """Extracts the 10-digit national number from an Indian phone string."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("91") and len(digits) == 12:
        return digits[2:]
    elif len(digits) == 10:
        return digits
    elif len(digits) > 10:
        return digits[-10:]
    return digits


async def send_sms_otp(phone: str, otp_code: str) -> tuple[bool, str]:
    """Sends a 6-digit OTP code to the given phone number via Fast2SMS.

    Args:
        phone: Mobile phone number (e.g. +919909437156 or 9909437156)
        otp_code: 6-digit OTP string

    Returns:
        tuple[bool, str]: (Success status, descriptive message/error)
    """
    clean_number = extract_10_digit_phone(phone)
    if len(clean_number) != 10:
        err = f"Invalid 10-digit mobile phone number: {phone}"
        logger.error(f"[SMS Gateway] {err}")
        return False, err

    api_key = getattr(settings, "FAST2SMS_API_KEY", "") or ""
    if not api_key:
        msg = f"[SMS Gateway] FAST2SMS_API_KEY is not configured in backend/.env"
        logger.warning(msg)
        return False, msg

    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": api_key.strip(),
        "Content-Type": "application/json",
    }
    payload = {
        "route": "otp",
        "variables_values": otp_code,
        "numbers": clean_number,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            logger.info(f"[SMS Gateway] Sending Fast2SMS OTP to {clean_number}...")
            response = await client.post(url, json=payload, headers=headers)
            res_data = response.json()

            if response.status_code == 200 and res_data.get("return") is True:
                req_id = res_data.get("request_id", "")
                logger.info(f"[SMS Gateway] Successfully sent OTP to {clean_number}. Request ID: {req_id}")
                return True, f"OTP dispatched to {clean_number} via Fast2SMS (Req: {req_id})"
            else:
                raw_msg = res_data.get("message") or response.text
                if isinstance(raw_msg, list):
                    raw_msg = " ".join(raw_msg)
                err_msg = f"Fast2SMS error: {raw_msg}"
                logger.error(f"[SMS Gateway] {err_msg}")
                return False, err_msg
    except Exception as e:
        err_msg = f"Fast2SMS connection error: {str(e)}"
        logger.error(f"[SMS Gateway] {err_msg}")
        return False, err_msg
