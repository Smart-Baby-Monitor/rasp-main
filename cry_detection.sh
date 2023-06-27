PREDICTION=0

function clean_up {
    # Perform program exit housekeeping
    echo ""
    echo "Thank you for using parenting 2.1"
    echo "Goodbye."
    exit
}

trap clean_up SIGHUP SIGINT SIGTERM

function predict() {
    echo "Predicting..."
    echo -n "What is the prediction? "
    python /opt/baby_cry_rpi/script/make_prediction.py
    PREDICTION=$(cat /opt/baby_cry_rpi/prediction/prediction.txt)
    echo "Prediction is $PREDICTION"
}

echo "Welcome to Parenting 2.1"
echo ""
while true; do
    predict
    echo "State of the Process: PREDICTION = $PREDICTION"
done
clean_up
