import sys
import requests
from pprint import pprint
import time
import random
from IPy import IP
#masks =  ["255.255.255.248", "255.255.255.240", "255.255.255.224", "255.255.255.192", "255.255.255.128", "255.255.255.0",
#		  "255.255.248.0", "255.255.240.0", "255.255.224.0", "255.255.192.0", "255.255.128.0", "255.255.0.0", ]


class IPAddrError(Exception):
	def __init__(self,err_type=-1):
		if err_type == 1:
			self.message = 'Private ip address!'
		else:
			self.message = 'Wrong ip address!'


class IP_Range(object):
	mask_start = 29
	mask_end = 24

	def __init__(self, mask_start = 29, mask_end = 24):
		self.mask_start = mask_start
		self.mask_end = mask_end
		self.masks = [x for x in range(self.mask_end, self.mask_start+1)]
		self.masks.reverse()

	def lookup_ipaddress_info(self, ip_address):
		print("Querying ip address for {}".format(ip_address))
		if ip_address == '1.119.1.40':
			return 20
		else:
			return random.randint(10,10)
		url = 'http://api.map.baidu.com/location/ip?ak=abDsBedrGw46lo1CyQuwZs9magjV5gSf&coor=&ip='+ ip_address
		r = None
		while r is None:
			try:
				r = requests.get(url, timeout=3)
			except requests.exceptions.ReadTimeout:
				print('Timtout!!!')
		if r.status_code != 200:
			return False
		r.encoding = 'utf-8'
		result = r.json()
		if result['status'] != 0:
			return False
		#data.pop('ip')
		return result['address']

	def check_ipaddr(self, ip_address):
		try:
			ip = IP(ip_address)
		except ValueError:
			raise IPAddrError(-1)
		if ip.iptype() == 'PRIVATE':
			raise IPAddrError(1)
		return ip

	def lookup_ip_range_info(self, ip_address, mask):
		#ip地址取29位掩码的网络地址、广播地址
		print("Querying network address for {}/{}".format(ip_address, mask))
		try:
			ip = self.check_ipaddr(ip_address)
		except IPAddrError as e:
			print(e.message)
		net_address = ip.make_net(mask).strNormal()
		ip_range = IP(net_address)
		boardcast_address = ip_range[-1]
		next_ipaddr = IP(boardcast_address.int()+1).strNormal(3)
		# print("{}, {}".format(ip_range.strNormal(3), next_ipaddr))
		# 查询ip地址
		ipaddr_info = {'ip_start': ip_range[0].strNormal(3),
					   'ip_range_int_start': ip_range[0].int(),
					   'ip_range_int_end': ip_range[-1].int(),
					   'ip_range': ip_range.strNormal(3),
					   'info': self.lookup_ipaddress_info(ip_address),
					   'netmask': mask,
					   'next_ip': next_ipaddr}
		#pprint(ipaddr_info)
		sleeptime = random.randint(3,8)/10
		print("Sleep {}s".format(sleeptime))
		time.sleep(sleeptime)
		return ipaddr_info


	def merge_network_address(self, start_ip):
		mask_step = 1
		merge_steps = 2
		ipaddr_info = self.lookup_ip_range_info(start_ip, self.masks[0])
		while mask_step < len(self.masks):
			print("{}  {}".format(2**(mask_step-1), merge_steps))
			for step in range(2**(mask_step-1), merge_steps):
				#print("  {}".format(step))
				next_ipaddr = ipaddr_info['next_ip']
				next_ipaddr_info = self.lookup_ip_range_info(next_ipaddr, self.masks[0])
				if ipaddr_info['info'] != next_ipaddr_info['info']:
					# 查询结果不同则返回网段信息
					yield megerd_ipaddr_info
					raise StopIteration
				ipaddr_info = next_ipaddr_info
			mask_step += 1
			net_address = IP(ipaddr_info['ip_start']).make_net(self.masks[mask_step-1]).strNormal()
			pprint("Merge IP range, New network address: {} , {}".format(net_address, self.masks[mask_step-1]))
			ipaddr_info = self.lookup_ip_range_info(ipaddr_info['ip_start'], self.masks[mask_step-1])
			megerd_ipaddr_info = ipaddr_info.copy()
			#yield merge_steps
			merge_steps = 2 ** mask_step
		yield ipaddr_info


if __name__ == '__main__':
	start_ip = sys.argv[1]
	ip_range = IP_Range(29, 24)
	ge = ip_range.merge_network_address(start_ip)
	try:
		while True:
			a1 = next(ge)
			pprint(a1)
	except StopIteration:
		print('end')



