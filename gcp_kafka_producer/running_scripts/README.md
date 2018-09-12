### Script illustrations

- kafka_produce.py
  Sending mocked messages to Kafka server

  1. Install package
  ```shell
  $ pip3 install kafka-python
  ```

  2. How to use:

  ```shell
  $ python3 kafka_produce.py --help
  usage: kafka_produce.py [-h] [--host HOST] [--topic TOPIC] [--thread THREAD]
                        [--timeunit TIMEUNIT] [--messages MESSAGES]
                        [--duration DURATION]

  optional arguments:
    -h, --help           show this help message and exit
    --host HOST          kafka server host
    --topic TOPIC        topic of the kafka
    --thread THREAD      thread number
    --timeunit TIMEUNIT  per (time unit) seconds
    --messages MESSAGES  send (messages) messages in (timeunit) seconds
    --duration DURATION  duration count
  ```

  3. Sample of use:
  ```shell
  $ python3 /home/shingyeong/kafka_produce.py \
  --host kafka.mlytics.us \
  --topic wafaccess \
  --thread 4 \
  --timeunit 1 \
  --duration 60 \
  --messages 100
  ```

- run_script_background.sh
  Running a command in the background several times

  1. How to use
  ```shell
  $ run_script_background.sh "<command>" <times>
  ```

  2. Sample of use:
  ```shell
  sh run_script_background.sh "sleep 3 && echo 123" 4
  ```
