<?php
    header('Content-type: application/json; charset=UTF-8');
    if(isset($_POST['update'])) {
        $ssid = $_POST['input1'];
        $pass = $_POST['input2'];
        shell_exec("sudo cp /var/tmp/interfaces.cl /etc/network/interfaces");
        shell_exec("sudo cp /var/tmp/dhcpcd.conf.cl /etc/dhcpcd.conf");
        shell_exec("sudo cp /var/tmp/hostapd.cl /etc/default/hostapd");
        //shell_exec("sudo cp /var/tmp/hizumi_4.conf.cl /etc/supervisor/conf.d/hizumi_4.conf");
        shell_exec("sudo chmod 666 /etc/wpa_supplicant/wpa_supplicant.conf");
        $fp = fopen("/etc/wpa_supplicant/wpa_supplicant.conf", "w");
        fwrite($fp,
"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
ssid=\"$ssid\"
psk=\"$pass\"
key_mgmt=WPA-PSK
}");
        fclose($fp);
        shell_exec("sudo iwconfig wlan0 essid $ssid key s:$pass");
        echo json_encode(array('status' => 'ok'));
        shell_exec("sudo shutdown -r now");
  }
  // MACアドレス取得
  if (isset($_POST['mac'])){
    $mac = shell_exec("ifconfig wlan0 | grep -o 'HWaddr\s*\([a-zA-Z0-9]\{2\}:\)\{5\}[a-zA-Z0-9]\{2\}'");
    $mac = trim(str_replace('HWaddr','',$mac));
    echo json_encode(array('status' => 'ok','mac' => $mac));
  }

?>
