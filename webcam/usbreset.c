/* usbreset -- send a USB port reset to a USB device
 *
 * Compile using: gcc -o usbreset usbreset.c
 *
 *
 *  https://gist.githubusercontent.com/x2q/5124616/raw/bf21dbda4a67de2c2d15d6c66b1e1bd0b1db7e1b/usbreset.c
 *
 * */

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

#include <linux/usbdevice_fs.h>


int main(int argc, char **argv)
{
	const char *filename;
	int fd;
	int rc;

	if (argc != 2) {
		fprintf(stderr, "Usage: usbreset device-filename\n");
		return 1;
	}
	filename = argv[1];

	fd = open(filename, O_WRONLY);
	if (fd < 0) {
		perror("Error opening output file");
		return 1;
	}

	printf("Resetting USB device %s\n", filename);
	rc = ioctl(fd, USBDEVFS_RESET, 0);
	if (rc < 0) {
		perror("Error in ioctl");
		return 1;
	}
	printf("Reset successful\n");

	close(fd);
	return 0;
}