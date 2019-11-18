import sys
import requests
from pprint import pprint
import time
import random
from IPy import IP
#masks =  ["255.255.255.248", "255.255.255.240", "255.255.255.224", "255.255.255.192", "255.255.255.128", "255.255.255.0",
#		  "255.255.248.0", "255.255.240.0", "255.255.224.0", "255.255.192.0", "255.255.128.0", "255.255.0.0", ]

mask_end = 24
mask_start = 29
masks = [x for x in range(mask_end,mask_start+1)]
masks.reverse()

class IPAddrError(Exception):
	def __init__(self,err_type=-1):
		if err_type == 1:
			self.message = 'Private ip address!'
		else:
			self.message = 'Wrong ip address!'


class IP_Range(object):
	@classmethod
	def lookup_ipaddress_info(cls, ip_address):
		print("Querying ip address for {}".format(ip_address))
		return random.randint(10,13)
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

	@classmethod
	def check_ipaddr(cls, ip_address):
		try:
			ip = IP(ip_address)
		except ValueError:
			raise IPAddrError(-1)
		if ip.iptype() == 'PRIVATE':
			raise IPAddrError(1)
		return ip

	@classmethod
	def lookup_ip_range_info(cls, ip_address, mask):
		#ip地址取29位掩码的网络地址、广播地址
		print("Querying network address for {}/{}".format(ip_address, mask))
		try:
			ip = cls.check_ipaddr(ip_address)
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
					   'info': cls.lookup_ipaddress_info(ip_address),
					   #'info': random.randint(10,13),
					   'next_ip': next_ipaddr}
		#pprint(ipaddr_info)
		sleeptime = random.randint(3,8)/10
		print("Sleep {}s".format(sleeptime))
		time.sleep(sleeptime)
		return ipaddr_info


	@classmethod
	def merge_network_address(cls, start_ip):
		mask_step = 1
		merge_steps = 2
		ipaddr_info = cls.lookup_ip_range_info(start_ip, masks[0])
		while mask_step < len(masks):
			print("{}  {}".format(2**(mask_step-1), merge_steps))
			for step in range(2**(mask_step-1), merge_steps):
				#print("  {}".format(step))
				next_ipaddr = ipaddr_info['next_ip']
				next_ipaddr_info = cls.lookup_ip_range_info(next_ipaddr, masks[0])
				if ipaddr_info['info'] != next_ipaddr_info['info']:
					# 查询结果不同则返回网段信息
					yield ipaddr_info
				ipaddr_info['info'] = next_ipaddr_info['info']
			mask_step += 1
			net_address = IP(ipaddr_info['ip_start']).make_net(masks[mask_step-1]).strNormal()
			ipaddr_info = cls.lookup_ip_range_info(ipaddr_info['ip_start'], masks[mask_step-1])
			pprint("Merge IP range, New network address: {} , {}".format(net_address, masks[mask_step-1]))
			#yield merge_steps
			merge_steps = 2 ** mask_step
		yield ipaddr_info


if __name__ == '__main__':
	start_ip = sys.argv[1]
	ge = IP_Range.merge_network_address(start_ip)
	try:
		while True:
			a1 = next(ge)
			pprint(a1)
	except StopIteration:
		print('end')



