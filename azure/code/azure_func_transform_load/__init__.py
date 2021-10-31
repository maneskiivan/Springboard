import datetime
import logging
import transform_load_venue_details
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    transform_load_venue_details.main()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
