RULE_PATH='.'
touch $RULE_PATH/fstone.rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", GROUP="root", MODE="0666"' > $RULE_PATH/fstone.rules