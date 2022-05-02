/************************************************************************* 
*
* Name: Antenna Data Module
* Project: Signal Analyzer
* Date: 17.02.2021
* Author: Jonas Buuck
*
**************************************************************************/

// ==[ INCLUDES ]=========================================================
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_event.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "nvs_flash.h"
#include "driver/uart.h"
#include "driver/gpio.h"

// ==[ DEFINES ]==========================================================
#define UART_RX_PIN (GPIO_NUM_4)
#define UART_TX_PIN (GPIO_NUM_2)
#define UART_RTS_PIN (UART_PIN_NO_CHANGE)
#define UART_CTS_PIN (UART_PIN_NO_CHANGE)

#define MAX_WIFI_NETWORKS_TO_DISCOVER (20) // size for array containing access point data

#define NETWORK_RECEIVED_BYTE 0x11 // byte received from raspberry after network transmission completed
#define SCAN_REQUEST_BYTE 0x22 // byte recevied from raspberry to initialze wifi scan

// ==[ APPLICATION ENTRY POINT ]==========================================
void app_main(void)
{
    // ==[ UART ]=========================================================
    // --< VARIABLES >-----
    uint8_t dataBuffer = 0; // container for bytes received via UART1
    int receivedBytes = 0; // variable for saving the number of bytes received in UART session

    // --< struct for UART configuration >-----
    uart_config_t uart_config = {
        .baud_rate = 19200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,  // disable flow control
        .source_clk = UART_SCLK_APB,            // use default clock
    };

    // --< install the UART driver: UART1, Rx Buffer Size = 2* FIFO length, Tx buffer size = 0 >-----
    uart_driver_install(UART_NUM_1, 1024 *2, 0, 0, NULL, 0);

    // --< set defined configuration for UART 1 >-----
    uart_param_config(UART_NUM_1, &uart_config);

    // --< assign pins for UART >-----
    uart_set_pin(UART_NUM_1, UART_TX_PIN, UART_RX_PIN, UART_RTS_PIN, UART_CTS_PIN);

    // ==[ NON-VOLATILE-STORAGE ]=====
    esp_err_t ret = nvs_flash_init();

    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK( ret );

    // ==[ NETWORK-SETUP ]================================================
    // --< VARIABLES >-----
    uint16_t sizeOfAccessPointStorageArray = MAX_WIFI_NETWORKS_TO_DISCOVER;
    uint16_t numberOfAccessPointsFound = 0;

    // --< array for containing access point data as structs >-----
    wifi_ap_record_t accessPointStorageArray[MAX_WIFI_NETWORKS_TO_DISCOVER];
    memset(accessPointStorageArray, 0, sizeof(accessPointStorageArray)); // initialize array

    // printf("size of storage array: %d\n" , sizeof(accessPointStorageArray));

    // --< set wifi configuration as default >-----
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();

    // --< initialize TCP/IP stack >-----
    ESP_ERROR_CHECK(esp_netif_init()); 
    ESP_ERROR_CHECK(esp_event_loop_create_default()); // create default system event loop, required for wifi-applications
    esp_netif_t *sta_netif = esp_netif_create_default_wifi_sta();
    assert(sta_netif);

    // --< initialize wifi with configuration >-----
    ESP_ERROR_CHECK(esp_wifi_init(&cfg)); 

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA)); // set mode to station
    ESP_ERROR_CHECK(esp_wifi_start()); // start WI-FI

    // ==[ MAIN LOOP]=====================================================
    while(1) {
        // --< wait for scan request >-----
        receivedBytes = uart_read_bytes(UART_NUM_1, &dataBuffer, 1, 20.0/portTICK_RATE_MS);
        
        // @DEBUG if(receivedBytes == 1) printf("Incoming request with code %d\n", dataBuffer);

        // --< if valid request comes in >-----
        if((receivedBytes == 1) && (dataBuffer == SCAN_REQUEST_BYTE)) {

            // --< run Wifi scan >-----
            // @DEBUG printf("running wifi scan\n");
            ESP_ERROR_CHECK(esp_wifi_scan_start(NULL, true)); // scan blocks program until scan is completed 

            // --< get access point records and store in array >-----
            ESP_ERROR_CHECK(esp_wifi_scan_get_ap_records(&sizeOfAccessPointStorageArray, accessPointStorageArray));
            
            // --< get number of access points found >-----
            ESP_ERROR_CHECK(esp_wifi_scan_get_ap_num(&numberOfAccessPointsFound));
            // @DEBUG printf("%d access points found\n", numberOfAccessPointsFound);

            // --< write number of access points to UART >-----
            uart_write_bytes(UART_NUM_1,(const char*)&numberOfAccessPointsFound,1);
            // @DEBUG printf("%d written to UART\n", numberOfAccessPointsFound);

            // --< receive validation to proceed >-----
            receivedBytes = uart_read_bytes(UART_NUM_1, &dataBuffer, 1, 2000.0/portTICK_RATE_MS);
            // @DEBUG printf("%d validation bytes received = %d\n", receivedBytes, dataBuffer);

            // --< restart main loop if no validation >-----
            if(receivedBytes == 0) 
            {
                // @DEBUG printf("Continue 1\n");
                continue;
            }
            if(dataBuffer != numberOfAccessPointsFound) 
            {
                // @DEBUG printf("Continue 2\n");
                uart_flush_input(UART_NUM_1);
                continue;
            }

            // --< write networks to UART >-----
            int i; 

            // --< iterate over number of access points found in current scan >-----
            for(i = 0; (i < numberOfAccessPointsFound) && (i < MAX_WIFI_NETWORKS_TO_DISCOVER); i++) 
            {
                // @DEBUG printf("running loop at i = %d\t\n", i);z

                // --< write RSSI value of network[i] to UART twice >-----
                uart_write_bytes(UART_NUM_1,(const char*)&accessPointStorageArray[i].rssi,1);
                uart_write_bytes(UART_NUM_1,(const char*)&accessPointStorageArray[i].rssi,1);

                // --< write ssid of network[i] to UART device >-----
                uart_write_bytes(UART_NUM_1,(const char*)accessPointStorageArray[i].ssid, 32);

                // --< wait for receive validation of raspberry >-----
                receivedBytes = uart_read_bytes(UART_NUM_1, &dataBuffer, 1, 2000.0/portTICK_RATE_MS);

                // @DEBUG printf("Received %d bytes, dataBuffer = %d \n", receivedBytes, dataBuffer);

                // --< if no validation or validation invalid, break out of sending loop >-----
                if(receivedBytes == 0) 
                {
                    // @DEBUG printf("Exiting loop 1\n");
                    break;
                }    
                if(dataBuffer != NETWORK_RECEIVED_BYTE) 
                {
                    // @DEBUG printf("Exiting loop 2\n");
                    uart_flush_input(UART_NUM_1);
                    break; 
                } 
            }

            // @DEBUG printf("\tloop ended with i = %d\n\n", i);

        }

        // --< if request is not valid, flush buffer >-----
        else{
            uart_flush_input(UART_NUM_1);
        }

    }
}
