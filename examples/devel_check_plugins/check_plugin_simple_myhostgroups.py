#!/usr/bin/env python3

# pylint: disable=missing-function-docstring

from .agent_based_api.v1 import register, Result, Service, State


def parse_myhostgroups(string_table):
    # string_table = [["check_mk", "myhost1,myhost2,myhost3,myhost4"],
    #  ["foo", "myhost11,myhost22,myhost33,myhost44"]]
    parsed = {}

    for line in string_table:
        parsed[line[0]] = {"members": line[1]}

    # parsed = {"check_mk": {"hosts": "myhost1,myhost2,myhost3,myhost4"},
    #  "foo": {"hosts": "myhost11,myhost22,myhost33,myhost44"}}
    return parsed


register.agent_section(
    name="myhostgroups",
    parse_function=parse_myhostgroups,
)


def discover_myhostgroups(section):
    yield Service()


def check_myhostgroups(section):
    attr = section.get("check_mk")
    hosts = attr["members"] if attr else ""
    if hosts:
        yield Result(state=State.CRIT, summary=f"Default group is not empty; Current member list: {hosts}")
    else:
        yield Result(state=State.OK, summary="Everything is fine")


register.check_plugin(
    name="myhostgroups",
    service_name="Hostgroup check_mk",
    discovery_function=discover_myhostgroups,
    check_function=check_myhostgroups,
)
